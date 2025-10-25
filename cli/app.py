"""
GWC-SIEM CLI Application
Command-line tool for log processing, analysis, and alert notification.
"""

import argparse
import sys
import json
from typing import Optional

# Import alert system modules
from core.detections.brute_force import detect_brute_force
from notifications.hooks import handle_alert


def process_logs(log_file: str, kind: str, output: Optional[str] = None):
    """Process logs and trigger alerts if detected."""
    try:
        with open(log_file, "r") as f:
            logs = json.load(f)
    except Exception as e:
        print(f"[error] Failed to read log file: {e}")
        return

    print(f"Processing {kind} log file: {log_file}")

    alerts = detect_brute_force(logs)
    for alert in alerts:
        print("⚠️ Alert Generated:", alert)
        try:
            handle_alert(alert)
        except Exception as e:
            print(f"[notifications] Failed to handle alert: {e}")

    if output:
        with open(output, "w") as f:
            json.dump(alerts, f, indent=2)
        print(f"Results saved to {output}")


def main(args: Optional[list] = None):
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="GWC-SIEM Command Line Interface", prog="gwc-siem"
    )

    parser.add_argument("--version", action="version", version="%(prog)s 1.0.0")

    parser.add_argument("--file", type=str, help="Log file to process")

    parser.add_argument(
        "--kind", type=str, choices=["auth", "nginx", "apache"], help="Type of log file"
    )

    parser.add_argument("--output", type=str, help="Output file for results")

    parser.add_argument(
        "--alert-test",
        action="store_true",
        help="Run alert notification system on sample logs",
    )

    if args is None:
        args = sys.argv[1:]

    parsed_args = parser.parse_args(args)

    if parsed_args.alert_test:
        process_logs("logs.json", "auth")
    elif parsed_args.file and parsed_args.kind:
        process_logs(parsed_args.file, parsed_args.kind, parsed_args.output)
    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
