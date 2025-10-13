
import argparse
import sys
import os

# Add the backend path to the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend')))

from app import parser, detector, db

def main():
    arg_parser = argparse.ArgumentParser(description="Mini-SIEM CLI")
    arg_parser.add_argument("--file", required=True, help="Path to the log file")
    arg_parser.add_argument("--kind", required=True, choices=["auth", "nginx", "apache"], help="Kind of log file")
    args = arg_parser.parse_args()

    try:
        parser_instance = parser.get_parser(args.kind)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        with open(args.file, "r") as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {args.file}", file=sys.stderr)
        sys.exit(1)

    events = []
    for line in lines:
        event = parser_instance.parse(line)
        if event:
            events.append(event)

    brute_force_detector = detector.BruteForceDetector()
    http_5xx_detector = detector.Http5xxBurstDetector()

    alerts = brute_force_detector.detect(events)
    alerts.extend(http_5xx_detector.detect(events))

    db.init_db()
    for alert in alerts:
        db.add_alert(alert)
        print(alert.json())

    print(f"\nIngested and analyzed {len(lines)} lines. Found {len(alerts)} alerts.")

if __name__ == "__main__":
    main()
