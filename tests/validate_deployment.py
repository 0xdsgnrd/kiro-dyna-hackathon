"""
Production deployment validation tests
"""
import asyncio
import time
import requests
import pytest
from typing import Dict, Any
import concurrent.futures
from dataclasses import dataclass

@dataclass
class ValidationResult:
    test_name: str
    passed: bool
    message: str
    duration: float
    details: Dict[str, Any] = None

class ProductionValidator:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.results = []
    
    def add_result(self, test_name: str, passed: bool, message: str, duration: float, details: Dict = None):
        """Add validation result"""
        result = ValidationResult(test_name, passed, message, duration, details or {})
        self.results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}: {message} ({duration:.2f}s)")
    
    def test_basic_connectivity(self) -> bool:
        """Test basic API connectivity"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                self.add_result("Basic Connectivity", True, "API is accessible", duration)
                return True
            else:
                self.add_result("Basic Connectivity", False, f"HTTP {response.status_code}", duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.add_result("Basic Connectivity", False, str(e), duration)
            return False
    
    def test_detailed_health(self) -> bool:
        """Test detailed health endpoint"""
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health/detailed", timeout=self.timeout)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                is_healthy = data.get('status') == 'healthy'
                db_connected = data.get('database', {}).get('connection', False)
                
                details = {
                    'status': data.get('status'),
                    'database_connected': db_connected,
                    'environment': data.get('environment'),
                    'version': data.get('version')
                }
                
                if is_healthy and db_connected:
                    self.add_result("Detailed Health", True, "All systems healthy", duration, details)
                    return True
                else:
                    self.add_result("Detailed Health", False, "System unhealthy", duration, details)
                    return False
            else:
                self.add_result("Detailed Health", False, f"HTTP {response.status_code}", duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.add_result("Detailed Health", False, str(e), duration)
            return False
    
    def test_api_endpoints(self) -> bool:
        """Test critical API endpoints"""
        endpoints = [
            ("/api/v1/auth/register", "POST"),
            ("/api/v1/auth/token", "POST"),
            ("/api/v1/content", "GET"),
            ("/api/v1/tags", "GET"),
            ("/api/v1/categories", "GET")
        ]
        
        all_passed = True
        for endpoint, method in endpoints:
            start_time = time.time()
            try:
                if method == "GET":
                    response = requests.get(f"{self.base_url}{endpoint}", timeout=self.timeout)
                else:
                    # For POST endpoints, expect 422 (validation error) or 401 (unauthorized)
                    response = requests.post(f"{self.base_url}{endpoint}", json={}, timeout=self.timeout)
                
                duration = time.time() - start_time
                
                # Accept various status codes that indicate the endpoint is working
                acceptable_codes = [200, 401, 422, 404] if method == "POST" else [200, 401]
                
                if response.status_code in acceptable_codes:
                    self.add_result(f"Endpoint {endpoint}", True, f"Responds correctly ({response.status_code})", duration)
                else:
                    self.add_result(f"Endpoint {endpoint}", False, f"HTTP {response.status_code}", duration)
                    all_passed = False
                    
            except Exception as e:
                duration = time.time() - start_time
                self.add_result(f"Endpoint {endpoint}", False, str(e), duration)
                all_passed = False
        
        return all_passed
    
    def test_performance(self) -> bool:
        """Test API performance under load"""
        start_time = time.time()
        
        def make_request():
            try:
                response = requests.get(f"{self.base_url}/health", timeout=5)
                return response.elapsed.total_seconds()
            except:
                return None
        
        # Make 10 concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            response_times = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        duration = time.time() - start_time
        valid_times = [t for t in response_times if t is not None]
        
        if len(valid_times) >= 8:  # At least 80% success rate
            avg_time = sum(valid_times) / len(valid_times)
            max_time = max(valid_times)
            
            details = {
                'success_rate': f"{len(valid_times)}/10",
                'avg_response_time': f"{avg_time:.3f}s",
                'max_response_time': f"{max_time:.3f}s"
            }
            
            if avg_time < 1.0 and max_time < 3.0:
                self.add_result("Performance Test", True, f"Good performance (avg: {avg_time:.3f}s)", duration, details)
                return True
            else:
                self.add_result("Performance Test", False, f"Slow performance (avg: {avg_time:.3f}s)", duration, details)
                return False
        else:
            self.add_result("Performance Test", False, f"High failure rate ({len(valid_times)}/10)", duration)
            return False
    
    def test_ssl_certificate(self) -> bool:
        """Test SSL certificate validity"""
        if not self.base_url.startswith('https://'):
            self.add_result("SSL Certificate", False, "Not using HTTPS", 0)
            return False
        
        start_time = time.time()
        try:
            response = requests.get(f"{self.base_url}/health", timeout=self.timeout, verify=True)
            duration = time.time() - start_time
            
            if response.status_code == 200:
                self.add_result("SSL Certificate", True, "Valid SSL certificate", duration)
                return True
            else:
                self.add_result("SSL Certificate", False, f"SSL error: HTTP {response.status_code}", duration)
                return False
        except requests.exceptions.SSLError as e:
            duration = time.time() - start_time
            self.add_result("SSL Certificate", False, f"SSL error: {str(e)}", duration)
            return False
        except Exception as e:
            duration = time.time() - start_time
            self.add_result("SSL Certificate", False, str(e), duration)
            return False
    
    def test_cors_headers(self) -> bool:
        """Test CORS configuration"""
        start_time = time.time()
        try:
            headers = {'Origin': 'https://your-frontend-domain.com'}
            response = requests.options(f"{self.base_url}/api/v1/content", headers=headers, timeout=self.timeout)
            duration = time.time() - start_time
            
            cors_headers = {
                'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
                'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
                'access-control-allow-headers': response.headers.get('access-control-allow-headers')
            }
            
            if any(cors_headers.values()):
                self.add_result("CORS Headers", True, "CORS configured", duration, cors_headers)
                return True
            else:
                self.add_result("CORS Headers", False, "No CORS headers found", duration)
                return False
        except Exception as e:
            duration = time.time() - start_time
            self.add_result("CORS Headers", False, str(e), duration)
            return False
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all validation tests"""
        print(f"🚀 Starting production validation for {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        
        # Run tests in order
        tests = [
            self.test_basic_connectivity,
            self.test_detailed_health,
            self.test_api_endpoints,
            self.test_performance,
            self.test_ssl_certificate,
            self.test_cors_headers
        ]
        
        passed_tests = 0
        for test in tests:
            if test():
                passed_tests += 1
        
        total_duration = time.time() - start_time
        
        print("=" * 60)
        print(f"📊 Validation Summary:")
        print(f"   Tests Passed: {passed_tests}/{len(tests)}")
        print(f"   Success Rate: {(passed_tests/len(tests)*100):.1f}%")
        print(f"   Total Duration: {total_duration:.2f}s")
        
        # Determine overall status
        if passed_tests == len(tests):
            print("🎉 All tests passed! Production deployment is ready.")
            status = "READY"
        elif passed_tests >= len(tests) * 0.8:
            print("⚠️  Most tests passed. Review failures before going live.")
            status = "REVIEW_REQUIRED"
        else:
            print("❌ Multiple test failures. Deployment needs fixes.")
            status = "NOT_READY"
        
        return {
            'status': status,
            'passed_tests': passed_tests,
            'total_tests': len(tests),
            'success_rate': passed_tests / len(tests),
            'duration': total_duration,
            'results': self.results
        }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python validate_deployment.py <api_url>")
        print("Example: python validate_deployment.py https://api.example.com")
        sys.exit(1)
    
    api_url = sys.argv[1]
    validator = ProductionValidator(api_url)
    summary = validator.run_all_tests()
    
    # Exit with appropriate code
    if summary['status'] == 'READY':
        sys.exit(0)
    elif summary['status'] == 'REVIEW_REQUIRED':
        sys.exit(1)
    else:
        sys.exit(2)
