from datetime import datetime

def detect_brute_force(logs):
    """Mock detection: triggers if >5 failed logins from same IP."""
    alerts = []
    ip_attempts = {}

    for log in logs:
        ip = log.get("ip")
        if log.get("status") == "failed":
            ip_attempts[ip] = ip_attempts.get(ip, 0) + 1
            if ip_attempts[ip] > 5:
                alert = {
                    "type": "ssh_brute_force",
                    "source_ip": ip,
                    "count": ip_attempts[ip],
                    "timestamp": datetime.utcnow().isoformat()
                }
                alerts.append(alert)
    return alerts
