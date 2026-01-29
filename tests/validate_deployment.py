#!/usr/bin/env python3

"""
Content Aggregator Platform - Deployment Validation Script
This script validates that the deployment is working correctly
"""

import requests
import json
import sys
import time
import argparse
from typing import Dict, List, Tuple

class DeploymentValidator:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.timeout = timeout
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {level}: {message}")
    
    def test_health_endpoint(self) -> Tuple[bool, str]:
        """Test basic health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                return True, "Health endpoint responding"
            else:
                return False, f"Health endpoint returned {response.status_code}"
        except Exception as e:
            return False, f"Health endpoint failed: {str(e)}"
    
    def test_detailed_health_endpoint(self) -> Tuple[bool, str]:
        """Test detailed health endpoint"""
        try:
            response = self.session.get(f"{self.base_url}/health/detailed")
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'healthy':
                    db_status = data.get('database', {}).get('connection', False)
                    if db_status:
                        return True, "Detailed health check passed"
                    else:
                        return False, "Database connection failed"
                else:
                    return False, f"Application status: {data.get('status')}"
            else:
                return False, f"Detailed health endpoint returned {response.status_code}"
        except Exception as e:
            return False, f"Detailed health endpoint failed: {str(e)}"
    
    def test_api_endpoints(self) -> List[Tuple[bool, str]]:
        """Test key API endpoints"""
        endpoints = [
            ("/api/v1/auth/register", "POST", {"email": "test@example.com", "username": "testuser", "password": "testpass123"}),
            ("/api/v1/categories", "GET", None),
            ("/api/v1/tags", "GET", None),
        ]
        
        results = []
        
        for endpoint, method, data in endpoints:
            try:
                if method == "GET":
                    response = self.session.get(f"{self.base_url}{endpoint}")
                elif method == "POST":
                    response = self.session.post(f"{self.base_url}{endpoint}", json=data)
                
                # Accept both success and auth-required responses
                if response.status_code in [200, 201, 401, 422]:
                    results.append((True, f"{method} {endpoint}: {response.status_code}"))
                else:
                    results.append((False, f"{method} {endpoint}: {response.status_code}"))
                    
            except Exception as e:
                results.append((False, f"{method} {endpoint}: {str(e)}"))
        
        return results
    
    def test_performance(self) -> Tuple[bool, str]:
        """Test response time performance"""
        try:
            start_time = time.time()
            response = self.session.get(f"{self.base_url}/health")
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200 and response_time < 2000:  # Less than 2 seconds
                return True, f"Response time: {response_time:.2f}ms"
            else:
                return False, f"Slow response time: {response_time:.2f}ms"
                
        except Exception as e:
            return False, f"Performance test failed: {str(e)}"
    
    def test_load_balancer_health(self) -> Tuple[bool, str]:
        """Test load balancer health by making multiple requests"""
        try:
            success_count = 0
            total_requests = 5
            
            for i in range(total_requests):
                response = self.session.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    success_count += 1
                time.sleep(0.5)  # Small delay between requests
            
            success_rate = (success_count / total_requests) * 100
            
            if success_rate >= 80:  # 80% success rate
                return True, f"Load balancer health: {success_rate}% success rate"
            else:
                return False, f"Load balancer issues: {success_rate}% success rate"
                
        except Exception as e:
            return False, f"Load balancer test failed: {str(e)}"
    
    def run_validation(self) -> bool:
        """Run all validation tests"""
        self.log("Starting deployment validation...")
        
        tests = [
            ("Health Endpoint", self.test_health_endpoint),
            ("Detailed Health", self.test_detailed_health_endpoint),
            ("Performance", self.test_performance),
            ("Load Balancer", self.test_load_balancer_health),
        ]
        
        all_passed = True
        
        for test_name, test_func in tests:
            self.log(f"Running {test_name} test...")
            success, message = test_func()
            
            if success:
                self.log(f"✅ {test_name}: {message}", "PASS")
            else:
                self.log(f"❌ {test_name}: {message}", "FAIL")
                all_passed = False
        
        # Run API endpoint tests
        self.log("Running API endpoint tests...")
        api_results = self.test_api_endpoints()
        
        for success, message in api_results:
            if success:
                self.log(f"✅ API: {message}", "PASS")
            else:
                self.log(f"❌ API: {message}", "FAIL")
                all_passed = False
        
        return all_passed
    
    def wait_for_deployment(self, max_wait_time: int = 300) -> bool:
        """Wait for deployment to be ready"""
        self.log(f"Waiting for deployment to be ready (max {max_wait_time}s)...")
        
        start_time = time.time()
        
        while time.time() - start_time < max_wait_time:
            try:
                response = self.session.get(f"{self.base_url}/health")
                if response.status_code == 200:
                    self.log("Deployment is ready!")
                    return True
            except:
                pass
            
            self.log("Deployment not ready yet, waiting 10s...")
            time.sleep(10)
        
        self.log("Deployment did not become ready in time", "ERROR")
        return False

def main():
    parser = argparse.ArgumentParser(description="Validate Content Aggregator deployment")
    parser.add_argument("--url", required=True, help="Base URL of the deployed application")
    parser.add_argument("--wait", action="store_true", help="Wait for deployment to be ready")
    parser.add_argument("--timeout", type=int, default=30, help="Request timeout in seconds")
    parser.add_argument("--max-wait", type=int, default=300, help="Maximum wait time for deployment")
    
    args = parser.parse_args()
    
    validator = DeploymentValidator(args.url, args.timeout)
    
    if args.wait:
        if not validator.wait_for_deployment(args.max_wait):
            sys.exit(1)
    
    if validator.run_validation():
        validator.log("🎉 All validation tests passed!", "SUCCESS")
        sys.exit(0)
    else:
        validator.log("💥 Some validation tests failed!", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()
