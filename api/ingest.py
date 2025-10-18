from flask import Flask, request, jsonify
from core.detections.brute_force import detect_brute_force
from notifications.hooks import handle_alert

app = Flask(__name__)

@app.route("/ingest", methods=["POST"])
def ingest_logs():
    data = request.json or []
    alerts = detect_brute_force(data)

    for alert in alerts:
        try:
            handle_alert(alert)
        except Exception as e:
            print(f"[notifications] failed to handle alert: {e}")

    return jsonify({"alerts_generated": len(alerts)}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)
