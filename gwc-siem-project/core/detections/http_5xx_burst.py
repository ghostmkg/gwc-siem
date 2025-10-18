
from datetime import timedelta

# Configuration
HTTP_5XX_THRESHOLD = 10
TIME_WINDOW = timedelta(minutes=1)

def detect_http_5xx_burst(events: list) -> list:
    """
    Detects a burst of HTTP 5xx errors from the same IP address.
    """
    alerts = []
    http_5xx_errors = {}

    for event in events:
        if isinstance(event.get('status'), int) and 500 <= event.get('status', 0) < 600:
            ip = event.get('ip')
            timestamp = event.get('timestamp')

            if ip not in http_5xx_errors:
                http_5xx_errors[ip] = []
            
            # Remove old events from the time window
            http_5xx_errors[ip] = [t for t in http_5xx_errors[ip] if timestamp - t <= TIME_WINDOW]
            
            http_5xx_errors[ip].append(timestamp)

            if len(http_5xx_errors[ip]) >= HTTP_5XX_THRESHOLD:
                alerts.append({
                    'type': 'http_5xx_burst',
                    'ip': ip,
                    'timestamp': timestamp,
                    'message': f'Multiple HTTP 5xx errors from {ip}'
                })
    return alerts
