import os
from datetime import datetime
from app.parsers import parse_nginx_line
from app.detectors import process_event
from app.storage import init_db, list_alerts, save_event

# --- initialize database ---
init_db()

# --- load log lines ---
LOG_FILE = r"C:\Users\KRUSHNALI\Downloads\nginx.log"
with open(LOG_FILE, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

# --- process lines ---
for line in lines:
    parsed = parse_nginx_line(line)
    if parsed:
        # Save event to DB
        save_event(timestamp=parsed["timestamp"], source=parsed.get("source", "nginx"),
                   raw=parsed["raw"], event_type=parsed["type"])
        # Run detector
        process_event(parsed)

# --- fetch alerts ---
alerts = list_alerts(limit=100)
print(f"Generated {len(alerts)} alerts:")
for a in alerts:
    print(f"[{a.timestamp}] {a.alert_type} from {a.source} -> {a.details}")
