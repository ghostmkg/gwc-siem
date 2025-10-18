import json
from core.detections.brute_force import detect_brute_force
from notifications.hooks import handle_alert

def run_cli(log_file="logs.json"):
    with open(log_file, "r") as f:
        logs = json.load(f)

    alerts = detect_brute_force(logs)
    for alert in alerts:
        print("⚠️ Alert Generated:", alert)
        try:
            handle_alert(alert)
        except Exception as e:
            print(f"[notifications] failed to handle alert: {e}")

if __name__ == "__main__":
    run_cli()
