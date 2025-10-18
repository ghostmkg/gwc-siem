# tests/test_notifications.py
import os
import json
from notifications.sender import NotificationManager

def test_from_config_tmp(tmp_path, monkeypatch):
    cfg = {
        "slack_webhook": "https://example.invalid/slack",
        "discord_webhook": "https://example.invalid/discord",
        "smtp": {
            "server": "smtp.example.invalid",
            "port": 465,
            "user": "u",
            "password": "p",
            "email_from": "from@example.invalid",
            "email_to": "to@example.invalid"
        },
        "rate_limit_seconds": 0
    }
    p = tmp_path / "config.json"
    p.write_text(json.dumps(cfg))
    nm = NotificationManager.from_config(str(p))
    assert nm.slack_webhook == cfg["slack_webhook"]
    assert nm.discord_webhook == cfg["discord_webhook"]
    assert nm.smtp_server == cfg["smtp"]["server"]
