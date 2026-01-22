#!/bin/bash

# Load testing script for production deployment validation
# Tests the application under various load conditions

set -e

API_URL=${1:-"http://localhost:8000"}
CONCURRENT_USERS=${2:-10}
DURATION=${3:-60}

echo "🔥 Load Testing: $API_URL"
echo "   Concurrent Users: $CONCURRENT_USERS"
echo "   Duration: ${DURATION}s"
echo "=" * 50

# Check if required tools are installed
command -v curl >/dev/null 2>&1 || { echo "curl is required but not installed."; exit 1; }

# Create load test script
cat > load_test.py << 'EOF'
#!/usr/bin/env python3
import asyncio
import aiohttp
import time
import json
import sys
from dataclasses import dataclass
from typing import List
import statistics

@dataclass
class RequestResult:
    status_code: int
    response_time: float
    success: bool
    error: str = None

class LoadTester:
    def __init__(self, base_url: str, concurrent_users: int, duration: int):
        self.base_url = base_url.rstrip('/')
        self.concurrent_users = concurrent_users
        self.duration = duration
        self.results: List[RequestResult] = []
        self.start_time = None
        self.running = True
    
    async def make_request(self, session: aiohttp.ClientSession, endpoint: str) -> RequestResult:
        """Make a single HTTP request"""
        start_time = time.time()
        try:
            async with session.get(f"{self.base_url}{endpoint}", timeout=aiohttp.ClientTimeout(total=10)) as response:
                response_time = time.time() - start_time
                return RequestResult(
                    status_code=response.status,
                    response_time=response_time,
                    success=200 <= response.status < 400
                )
        except Exception as e:
            response_time = time.time() - start_time
            return RequestResult(
                status_code=0,
                response_time=response_time,
                success=False,
                error=str(e)
            )
    
    async def user_simulation(self, user_id: int):
        """Simulate a single user's behavior"""
        endpoints = [
            "/health",
            "/health/detailed",
            "/api/v1/content",
            "/api/v1/tags",
            "/api/v1/categories"
        ]
        
        async with aiohttp.ClientSession() as session:
            while self.running and (time.time() - self.start_time) < self.duration:
                # Simulate user behavior - mix of endpoints
                for endpoint in endpoints:
                    if not self.running:
                        break
                    
                    result = await self.make_request(session, endpoint)
                    self.results.append(result)
                    
                    # Small delay between requests (simulate user think time)
                    await asyncio.sleep(0.1)
                
                # Longer pause between sessions
                await asyncio.sleep(1)
    
    async def run_load_test(self):
        """Run the load test"""
        print(f"Starting load test with {self.concurrent_users} concurrent users...")
        self.start_time = time.time()
        
        # Create tasks for concurrent users
        tasks = []
        for i in range(self.concurrent_users):
            task = asyncio.create_task(self.user_simulation(i))
            tasks.append(task)
        
        # Wait for duration or completion
        try:
            await asyncio.wait_for(asyncio.gather(*tasks), timeout=self.duration + 10)
        except asyncio.TimeoutError:
            pass
        finally:
            self.running = False
        
        # Cancel any remaining tasks
        for task in tasks:
            if not task.done():
                task.cancel()
        
        return self.analyze_results()
    
    def analyze_results(self) -> dict:
        """Analyze load test results"""
        if not self.results:
            return {"error": "No results collected"}
        
        total_requests = len(self.results)
        successful_requests = sum(1 for r in self.results if r.success)
        failed_requests = total_requests - successful_requests
        
        response_times = [r.response_time for r in self.results if r.success]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            p95_response_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
            max_response_time = max(response_times)
        else:
            avg_response_time = p95_response_time = max_response_time = 0
        
        # Calculate requests per second
        actual_duration = time.time() - self.start_time
        rps = total_requests / actual_duration if actual_duration > 0 else 0
        
        # Status code distribution
        status_codes = {}
        for result in self.results:
            code = result.status_code
            status_codes[code] = status_codes.get(code, 0) + 1
        
        return {
            "total_requests": total_requests,
            "successful_requests": successful_requests,
            "failed_requests": failed_requests,
            "success_rate": (successful_requests / total_requests) * 100 if total_requests > 0 else 0,
            "avg_response_time": avg_response_time,
            "p95_response_time": p95_response_time,
            "max_response_time": max_response_time,
            "requests_per_second": rps,
            "duration": actual_duration,
            "status_codes": status_codes
        }

async def main():
    if len(sys.argv) < 4:
        print("Usage: python load_test.py <url> <concurrent_users> <duration>")
        sys.exit(1)
    
    url = sys.argv[1]
    users = int(sys.argv[2])
    duration = int(sys.argv[3])
    
    tester = LoadTester(url, users, duration)
    results = await tester.run_load_test()
    
    print("\n" + "="*60)
    print("📊 LOAD TEST RESULTS")
    print("="*60)
    print(f"Total Requests: {results['total_requests']}")
    print(f"Successful: {results['successful_requests']}")
    print(f"Failed: {results['failed_requests']}")
    print(f"Success Rate: {results['success_rate']:.1f}%")
    print(f"Requests/Second: {results['requests_per_second']:.1f}")
    print(f"Avg Response Time: {results['avg_response_time']:.3f}s")
    print(f"95th Percentile: {results['p95_response_time']:.3f}s")
    print(f"Max Response Time: {results['max_response_time']:.3f}s")
    print(f"Test Duration: {results['duration']:.1f}s")
    
    print("\nStatus Code Distribution:")
    for code, count in results['status_codes'].items():
        print(f"  {code}: {count}")
    
    # Determine if test passed
    success_rate = results['success_rate']
    avg_response = results['avg_response_time']
    p95_response = results['p95_response_time']
    
    print("\n" + "="*60)
    if success_rate >= 95 and avg_response < 1.0 and p95_response < 2.0:
        print("✅ LOAD TEST PASSED - System performs well under load")
        sys.exit(0)
    elif success_rate >= 90 and avg_response < 2.0:
        print("⚠️  LOAD TEST WARNING - Acceptable performance with some issues")
        sys.exit(1)
    else:
        print("❌ LOAD TEST FAILED - System cannot handle the load")
        sys.exit(2)

if __name__ == "__main__":
    asyncio.run(main())
EOF

# Run the load test
python3 load_test.py "$API_URL" "$CONCURRENT_USERS" "$DURATION"

# Cleanup
rm -f load_test.py

echo ""
echo "Load testing completed!"
