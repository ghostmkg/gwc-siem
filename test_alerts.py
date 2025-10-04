# test_alerts.py
from app.parsers import parse_nginx_line
from app.detectors import process_event
from app.storage import list_alerts, init_db
from datetime import datetime, timedelta

# Initialize DB (so alerts table exists)
init_db()

# Simulated log lines (5xx responses to trigger alert)
test_lines = [
    '127.0.0.1 - - [01/Jan/2025:12:10:01 +0000] "GET /login HTTP/1.1" 500 1024 "-" "Mozilla/5.0"',
    '127.0.0.1 - - [01/Jan/2025:12:10:02 +0000] "GET /api/data HTTP/1.1" 502 768 "-" "Mozilla/5.0"',
    '127.0.0.1 - - [01/Jan/2025:12:10:03 +0000] "GET /dashboard HTTP/1.1" 503 820 "-" "Mozilla/5.0"',
]

print("Processing test lines...")

for line in test_lines:
    parsed = parse_nginx_line(line)
    if parsed:
        # force timestamp to now to avoid sliding window removing it
        parsed['timestamp'] = datetime.utcnow()
        process_event(parsed)

# Fetch alerts from DB
alerts = list_alerts(limit=10)
print("\nGenerated alerts:")
for a in alerts:
    print(f"{a.timestamp} | {a.alert_type} | {a.source} | {a.details}")
