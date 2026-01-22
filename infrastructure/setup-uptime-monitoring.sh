#!/bin/bash

# Uptime monitoring setup script
# Sets up external monitoring for the application

set -e

PROJECT_NAME="content-aggregator"
ENVIRONMENT="prod"
API_ENDPOINT="https://your-api-domain.com"

echo "Setting up uptime monitoring for $PROJECT_NAME..."

# Create uptime monitoring script
cat > uptime_monitor.py << 'EOF'
#!/usr/bin/env python3
"""
Simple uptime monitoring script
Checks application health and sends alerts if down
"""
import requests
import time
import json
import boto3
from datetime import datetime

class UptimeMonitor:
    def __init__(self, endpoint, alert_topic_arn=None):
        self.endpoint = endpoint
        self.alert_topic_arn = alert_topic_arn
        self.sns = boto3.client('sns') if alert_topic_arn else None
        self.consecutive_failures = 0
        self.max_failures = 3
    
    def check_health(self):
        """Check application health"""
        try:
            response = requests.get(f"{self.endpoint}/health", timeout=10)
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def check_detailed_health(self):
        """Check detailed application health"""
        try:
            response = requests.get(f"{self.endpoint}/health/detailed", timeout=15)
            if response.status_code == 200:
                data = response.json()
                return data.get('status') == 'healthy', data
            else:
                return False, f"HTTP {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, str(e)
    
    def send_alert(self, message):
        """Send alert via SNS"""
        if not self.sns or not self.alert_topic_arn:
            print(f"ALERT: {message}")
            return
        
        try:
            self.sns.publish(
                TopicArn=self.alert_topic_arn,
                Subject=f"Content Aggregator Alert - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                Message=message
            )
            print(f"Alert sent: {message}")
        except Exception as e:
            print(f"Failed to send alert: {e}")
    
    def monitor(self):
        """Main monitoring loop"""
        print(f"Starting uptime monitoring for {self.endpoint}")
        
        while True:
            try:
                # Basic health check
                is_healthy, result = self.check_health()
                
                if is_healthy:
                    if self.consecutive_failures > 0:
                        self.send_alert(f"Service recovered after {self.consecutive_failures} failures")
                    self.consecutive_failures = 0
                    print(f"✓ Health check passed: {result}")
                else:
                    self.consecutive_failures += 1
                    print(f"✗ Health check failed ({self.consecutive_failures}/{self.max_failures}): {result}")
                    
                    if self.consecutive_failures >= self.max_failures:
                        self.send_alert(f"Service is DOWN! {self.consecutive_failures} consecutive failures. Last error: {result}")
                
                # Detailed health check every 5 minutes
                if int(time.time()) % 300 == 0:
                    is_detailed_healthy, detailed_result = self.check_detailed_health()
                    if not is_detailed_healthy:
                        print(f"⚠ Detailed health check failed: {detailed_result}")
                    else:
                        db_status = detailed_result.get('database', {})
                        perf = db_status.get('performance', {})
                        if perf.get('response_time_ms', 0) > 1000:
                            print(f"⚠ Slow database response: {perf.get('response_time_ms')}ms")
                
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped")
                break
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python uptime_monitor.py <api_endpoint> [sns_topic_arn]")
        sys.exit(1)
    
    endpoint = sys.argv[1]
    topic_arn = sys.argv[2] if len(sys.argv) > 2 else None
    
    monitor = UptimeMonitor(endpoint, topic_arn)
    monitor.monitor()
EOF

chmod +x uptime_monitor.py

# Create systemd service for uptime monitoring
cat > content-aggregator-monitor.service << EOF
[Unit]
Description=Content Aggregator Uptime Monitor
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/opt/monitoring
ExecStart=/usr/bin/python3 /opt/monitoring/uptime_monitor.py $API_ENDPOINT
Restart=always
RestartSec=30

[Install]
WantedBy=multi-user.target
EOF

echo "Uptime monitoring setup complete!"
echo ""
echo "To deploy the monitoring:"
echo "1. Copy uptime_monitor.py to your monitoring server"
echo "2. Install the systemd service:"
echo "   sudo cp content-aggregator-monitor.service /etc/systemd/system/"
echo "   sudo systemctl enable content-aggregator-monitor"
echo "   sudo systemctl start content-aggregator-monitor"
echo ""
echo "To run manually:"
echo "   python3 uptime_monitor.py $API_ENDPOINT [SNS_TOPIC_ARN]"
