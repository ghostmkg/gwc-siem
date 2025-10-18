
import re
from datetime import timedelta

# Configuration
FAILED_LOGIN_THRESHOLD = 5
TIME_WINDOW = timedelta(minutes=5)

def detect_brute_force(events: list) -> list:
    """
    Detects brute force attacks based on multiple failed login attempts from the same IP address.
    """
    alerts = []
    failed_logins = {}

    for event in events:
        if event.get('process') == 'sshd' and 'Failed password' in event.get('message', ''):
            ip_match = re.search(r'from (\S+)', event['message'])
            if ip_match:
                ip = ip_match.group(1)
                timestamp = event['timestamp']

                if ip not in failed_logins:
                    failed_logins[ip] = []
                
                # Remove old events from the time window
                failed_logins[ip] = [t for t in failed_logins[ip] if timestamp - t < TIME_WINDOW]
                
                failed_logins[ip].append(timestamp)

                if len(failed_logins[ip]) >= FAILED_LOGIN_THRESHOLD:
                    alerts.append({
                        'type': 'brute_force',
                        'ip': ip,
                        'timestamp': timestamp,
                        'message': f'Multiple failed login attempts from {ip}'
                    })
    return alerts
