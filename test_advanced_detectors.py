#!/usr/bin/env python3
"""
Test script for advanced security detectors in Mini-SIEM
"""

import sys
import os
from datetime import datetime, timedelta

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.detectors import process_event
from app.storage import init_db, list_alerts

def test_sql_injection_detection():
    """Test SQL injection detection"""
    print("🧪 Testing SQL injection detection...")
    
    # Simulate SQL injection attempts
    sql_payloads = [
        "?id=1' OR '1'='1",
        "?user=admin' UNION SELECT * FROM users--",
        "?search=test'; DROP TABLE users;--",
        "?id=1 AND 1=1",
        "?query=test' OR 1=1--"
    ]
    
    for i, payload in enumerate(sql_payloads):
        event = {
            "timestamp": datetime.utcnow() - timedelta(seconds=i*10),
            "type": "nginx.access",
            "ip": "192.168.1.100",
            "path": f"/api/search{payload}",
            "status": 200,
            "method": "GET",
            "ua": "Mozilla/5.0"
        }
        process_event(event)
    
    print("✅ SQL injection test completed")

def test_suspicious_path_detection():
    """Test suspicious path detection"""
    print("🧪 Testing suspicious path detection...")
    
    suspicious_paths = [
        "/admin/login",
        "/wp-admin/",
        "/.env",
        "/config/database.php",
        "/backup/db.sql",
        "/.git/config",
        "/shell.php",
        "/cmd.exe",
        "/api/admin/users"
    ]
    
    for i, path in enumerate(suspicious_paths):
        event = {
            "timestamp": datetime.utcnow() - timedelta(seconds=i*5),
            "type": "nginx.access",
            "ip": "192.168.1.101",
            "path": path,
            "status": 404,
            "method": "GET",
            "ua": "Mozilla/5.0"
        }
        process_event(event)
    
    print("✅ Suspicious path test completed")

def test_user_enumeration_detection():
    """Test user enumeration detection"""
    print("🧪 Testing user enumeration detection...")
    
    enum_paths = [
        "/user/admin",
        "/users/john",
        "/profile/root",
        "/account/administrator",
        "/api/users/list",
        "/admin/users",
        "/members/alice"
    ]
    
    for i, path in enumerate(enum_paths):
        event = {
            "timestamp": datetime.utcnow() - timedelta(seconds=i*3),
            "type": "nginx.access",
            "ip": "192.168.1.102",
            "path": path,
            "status": 200,
            "method": "GET",
            "ua": "Mozilla/5.0"
        }
        process_event(event)
    
    print("✅ User enumeration test completed")

def test_unusual_user_agent_detection():
    """Test unusual user agent detection"""
    print("🧪 Testing unusual user agent detection...")
    
    unusual_agents = [
        "sqlmap/1.0",
        "nmap/7.80",
        "nikto/2.1.6",
        "python-requests/2.25.1",
        "go-http-client/1.1",
        "bot",
        "scanner",
        "",  # Empty user agent
        "a" * 600  # Very long user agent
    ]
    
    for i, ua in enumerate(unusual_agents):
        event = {
            "timestamp": datetime.utcnow() - timedelta(seconds=i*2),
            "type": "nginx.access",
            "ip": "192.168.1.103",
            "path": "/",
            "status": 200,
            "method": "GET",
            "ua": ua
        }
        process_event(event)
    
    print("✅ Unusual user agent test completed")

def test_port_scan_detection():
    """Test port scan detection via SSH"""
    print("🧪 Testing port scan detection...")
    
    # Simulate multiple users attempting SSH login from same IP
    users = ["admin", "root", "user", "test", "guest", "administrator"]
    
    for i, user in enumerate(users):
        event = {
            "timestamp": datetime.utcnow() - timedelta(seconds=i*5),
            "type": "ssh.failed_password",
            "ip": "192.168.1.104",
            "user": user,
            "source": "192.168.1.104"
        }
        process_event(event)
    
    print("✅ Port scan test completed")

def test_http_4xx_burst_detection():
    """Test HTTP 4xx error burst detection"""
    print("🧪 Testing HTTP 4xx burst detection...")
    
    # Simulate multiple 4xx errors from same IP
    for i in range(15):
        event = {
            "timestamp": datetime.utcnow() - timedelta(seconds=i*2),
            "type": "nginx.access",
            "ip": "192.168.1.105",
            "path": f"/nonexistent{i}",
            "status": 404,
            "method": "GET",
            "ua": "Mozilla/5.0"
        }
        process_event(event)
    
    print("✅ HTTP 4xx burst test completed")

def main():
    """Run all detector tests"""
    print("🚀 Starting Advanced Security Detector Tests")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    # Run all tests
    test_sql_injection_detection()
    test_suspicious_path_detection()
    test_user_enumeration_detection()
    test_unusual_user_agent_detection()
    test_port_scan_detection()
    test_http_4xx_burst_detection()
    
    print("\n" + "=" * 50)
    print("📊 Test Results - Generated Alerts:")
    print("=" * 50)
    
    # Display generated alerts
    alerts = list_alerts(50)
    if alerts:
        for alert in alerts:
            print(f"🚨 {alert['alert_type']} from {alert['source']}")
            print(f"   Time: {alert['timestamp']}")
            print(f"   Details: {alert['details']}")
            print()
    else:
        print("No alerts generated.")
    
    print(f"✅ All tests completed! Generated {len(alerts)} alerts.")

if __name__ == "__main__":
    main()
