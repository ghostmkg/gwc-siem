from collections import deque, defaultdict
from datetime import datetime, timedelta
from typing import Dict, Any, Set
from .storage import save_alert
import yaml, os
import re

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

# Existing detectors
ssh_failures: Dict[str, deque] = defaultdict(deque)
http_5xx: Dict[str, deque] = defaultdict(deque)

# New advanced detectors
http_4xx: Dict[str, deque] = defaultdict(deque)
suspicious_paths: Dict[str, deque] = defaultdict(deque)
user_enumeration: Dict[str, deque] = defaultdict(deque)
sql_injection_attempts: Dict[str, deque] = defaultdict(deque)
port_scan_attempts: Dict[str, Set[str]] = defaultdict(set)
unusual_user_agents: Dict[str, deque] = defaultdict(deque)

def _trim_deque(d: deque, window_seconds: int):
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window_seconds)
    while d and d[0] < cutoff:
        d.popleft()

def process_event(parsed: Dict[str, Any]):
    now = datetime.utcnow()
    
    # SSH Brute Force Detection
    if parsed.get("type") == "ssh.failed_password":
        ip = parsed.get("ip") or parsed.get("source")
        cfg = config["detectors"]["ssh_bruteforce"]
        dq = ssh_failures[ip]
        dq.append(parsed.get("timestamp", now))
        _trim_deque(dq, cfg["window_seconds"])
        if len(dq) >= cfg["attempts_threshold"]:
            save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="ssh_bruteforce",
                       details=f"{len(dq)} failed SSH attempts from {ip}")
            dq.clear()
    
    # HTTP 5xx Server Error Burst Detection
    if parsed.get("type") == "nginx.access":
        status = int(parsed.get("status", 0))
        ip = parsed.get("ip", "unknown")
        path = parsed.get("path", "")
        user_agent = parsed.get("ua", "")
        
        # 5xx Server Errors
        if 500 <= status <= 599:
            cfg = config["detectors"]["http_5xx_burst"]
            dq = http_5xx[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["errors_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="http_5xx_burst",
                           details=f"{len(dq)} HTTP 5xx responses from {ip}")
                dq.clear()
        
        # 4xx Client Error Burst Detection
        elif 400 <= status <= 499:
            cfg = config["detectors"]["http_4xx_burst"]
            dq = http_4xx[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["errors_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="http_4xx_burst",
                           details=f"{len(dq)} HTTP 4xx responses from {ip}")
                dq.clear()
        
        # Suspicious Path Detection
        if _is_suspicious_path(path):
            cfg = config["detectors"]["suspicious_paths"]
            dq = suspicious_paths[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["attempts_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="suspicious_paths",
                           details=f"{len(dq)} suspicious path accesses: {path}")
                dq.clear()
        
        # SQL Injection Detection
        if _contains_sql_injection(path):
            cfg = config["detectors"]["sql_injection"]
            dq = sql_injection_attempts[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["attempts_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="sql_injection",
                           details=f"{len(dq)} SQL injection attempts from {ip}")
                dq.clear()
        
        # User Enumeration Detection
        if _is_user_enumeration_attempt(path):
            cfg = config["detectors"]["user_enumeration"]
            dq = user_enumeration[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["attempts_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="user_enumeration",
                           details=f"{len(dq)} user enumeration attempts from {ip}")
                dq.clear()
        
        # Unusual User Agent Detection
        if _is_unusual_user_agent(user_agent):
            cfg = config["detectors"]["unusual_user_agents"]
            dq = unusual_user_agents[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["attempts_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="unusual_user_agents",
                           details=f"{len(dq)} requests with unusual user agents from {ip}")
                dq.clear()
    
    # Port Scan Detection (SSH)
    if parsed.get("type") == "ssh.failed_password":
        ip = parsed.get("ip") or parsed.get("source")
        user = parsed.get("user", "")
        cfg = config["detectors"]["port_scan"]
        
        # Track unique users attempted per IP
        port_scan_attempts[ip].add(user)
        
        # Check if too many different users attempted
        if len(port_scan_attempts[ip]) >= cfg["unique_users_threshold"]:
            save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="port_scan",
                       details=f"Port scan detected: {len(port_scan_attempts[ip])} unique users attempted from {ip}")
            port_scan_attempts[ip].clear()


def _is_suspicious_path(path: str) -> bool:
    """Check if the path contains suspicious patterns"""
    suspicious_patterns = [
        r'/admin', r'/wp-admin', r'/administrator', r'/phpmyadmin',
        r'/\.env', r'/config', r'/backup', r'/\.git',
        r'/\.ssh', r'/\.htaccess', r'/\.htpasswd',
        r'/shell', r'/cmd', r'/exec', r'/eval',
        r'/\.\./', r'/\.\.\\',  # Directory traversal
        r'/api/v1/admin', r'/api/admin', r'/admin/api'
    ]
    
    for pattern in suspicious_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def _contains_sql_injection(path: str) -> bool:
    """Check if the path contains SQL injection patterns"""
    sql_patterns = [
        r'union\s+select', r'select\s+.*\s+from', r'insert\s+into',
        r'delete\s+from', r'drop\s+table', r'update\s+.*\s+set',
        r'or\s+1\s*=\s*1', r'and\s+1\s*=\s*1', r';\s*drop',
        r'exec\s*\(', r'execute\s*\(', r'sp_', r'xp_',
        r'waitfor\s+delay', r'benchmark\s*\(', r'sleep\s*\('
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def _is_user_enumeration_attempt(path: str) -> bool:
    """Check if the path indicates user enumeration attempts"""
    enum_patterns = [
        r'/user/', r'/users/', r'/profile/', r'/account/',
        r'/login\?user=', r'/login\?username=', r'/api/users/',
        r'/admin/users', r'/members/', r'/accounts/'
    ]
    
    for pattern in enum_patterns:
        if re.search(pattern, path, re.IGNORECASE):
            return True
    return False


def _is_unusual_user_agent(user_agent: str) -> bool:
    """Check if the user agent is unusual or suspicious"""
    if not user_agent or user_agent == '-':
        return True
    
    suspicious_agents = [
        r'sqlmap', r'nmap', r'nikto', r'wget', r'curl',
        r'python-requests', r'go-http-client', r'java/',
        r'bot', r'crawler', r'spider', r'scanner',
        r'nikto', r'nessus', r'openvas', r'burp'
    ]
    
    for pattern in suspicious_agents:
        if re.search(pattern, user_agent, re.IGNORECASE):
            return True
    
    # Check for very short or very long user agents
    if len(user_agent) < 10 or len(user_agent) > 500:
        return True
    
    return False
