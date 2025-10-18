# notifications/sender.py
"""
Notification manager supporting Slack, Discord, Email.
Usage:
    nm = NotificationManager.from_config("config/config.json")
    nm.notify(event)
"""

import json
import os
import time
import threading
from typing import Optional, Dict, Any
from pathlib import Path

import requests
import smtplib
from email.mime.text import MIMEText

# Simple in-memory rate limiter to prevent spamming same alert repeatedly
class RateLimiter:
    def __init__(self, cooldown_seconds: int = 60):
        # key -> last_sent_timestamp
        self._last = {}
        self._cooldown = cooldown_seconds
        self._lock = threading.Lock()

    def can_send(self, key: str) -> bool:
        now = time.time()
        with self._lock:
            last = self._last.get(key, 0)
            if now - last >= self._cooldown:
                self._last[key] = now
                return True
            return False

class NotificationManager:
    def __init__(self,
                 slack_webhook: Optional[str] = None,
                 discord_webhook: Optional[str] = None,
                 smtp_server: Optional[str] = None,
                 smtp_port: Optional[int] = None,
                 smtp_user: Optional[str] = None,
                 smtp_password: Optional[str] = None,
                 email_from: Optional[str] = None,
                 email_to: Optional[str] = None,
                 rate_limit_seconds: int = 60):
        self.slack_webhook = slack_webhook
        self.discord_webhook = discord_webhook
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user
        self.smtp_password = smtp_password
        self.email_from = email_from
        self.email_to = email_to

        self.rate_limiter = RateLimiter(rate_limit_seconds)

    @classmethod
    def from_config(cls, path: str = "config/config.json"):
        cfg_path = Path(path)
        if not cfg_path.exists():
            # try environment variables as fallback
            return cls(
                slack_webhook=os.environ.get("SLACK_WEBHOOK"),
                discord_webhook=os.environ.get("DISCORD_WEBHOOK"),
                smtp_server=os.environ.get("SMTP_SERVER"),
                smtp_port=int(os.environ.get("SMTP_PORT", "465")) if os.environ.get("SMTP_SERVER") else None,
                smtp_user=os.environ.get("SMTP_USER"),
                smtp_password=os.environ.get("SMTP_PASSWORD"),
                email_from=os.environ.get("EMAIL_FROM"),
                email_to=os.environ.get("EMAIL_TO"),
            )
        with cfg_path.open() as fh:
            cfg = json.load(fh)
        return cls(
            slack_webhook=cfg.get("slack_webhook"),
            discord_webhook=cfg.get("discord_webhook"),
            smtp_server=cfg.get("smtp", {}).get("server"),
            smtp_port=cfg.get("smtp", {}).get("port"),
            smtp_user=cfg.get("smtp", {}).get("user"),
            smtp_password=cfg.get("smtp", {}).get("password"),
            email_from=cfg.get("smtp", {}).get("email_from"),
            email_to=cfg.get("smtp", {}).get("email_to"),
            rate_limit_seconds=cfg.get("rate_limit_seconds", 60)
        )

    def _format_message(self, event: Dict[str, Any]) -> str:
        # Standard human-friendly text
        parts = []
        ev_type = event.get("type") or event.get("alert_type") or "unknown"
        parts.append(f"**SIEM Alert:** {ev_type}")
        if "source_ip" in event:
            parts.append(f"Source IP: {event['source_ip']}")
        if "username" in event:
            parts.append(f"User: {event['username']}")
        if "count" in event:
            parts.append(f"Count: {event['count']}")
        if "timestamp" in event:
            parts.append(f"Time: {event['timestamp']}")
        # attach raw message if present
        if "raw" in event:
            parts.append(f"Raw: {event['raw']}")
        return "\n".join(parts)

    def _make_spam_key(self, event: Dict[str, Any]) -> str:
        # key for rate limiting: type + source_ip
        return f"{event.get('type')}-{event.get('source_ip')}"

    def notify(self, event: Dict[str, Any]) -> None:
        """
        High-level function to send notifications across configured channels.
        Non-blocking for network calls: spawns background threads to send.
        Applies a simple rate-limit based on event type+ip to avoid spam.
        """
        if not event:
            return

        key = self._make_spam_key(event)
        if not self.rate_limiter.can_send(key):
            # skip to avoid spamming
            return

        text = self._format_message(event)

        # send concurrently
        threads = []
        if self.slack_webhook:
            t = threading.Thread(target=self._send_slack, args=(text, self.slack_webhook))
            t.start(); threads.append(t)
        if self.discord_webhook:
            t = threading.Thread(target=self._send_discord, args=(text, self.discord_webhook))
            t.start(); threads.append(t)
        if self.smtp_server and self.email_to and self.email_from:
            t = threading.Thread(target=self._send_email, args=(event, text))
            t.start(); threads.append(t)

        # optionally wait a short time for threads to begin to surface errors quickly in logs
        for t in threads:
            t.join(0.1)

    def _send_slack(self, message: str, webhook: str):
        payload = {"text": message}
        try:
            resp = requests.post(webhook, json=payload, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            # avoid raising in background thread; log
            print(f"[notifications] Slack send failed: {e}")

    def _send_discord(self, message: str, webhook: str):
        payload = {"content": message}
        try:
            resp = requests.post(webhook, json=payload, timeout=5)
            resp.raise_for_status()
        except Exception as e:
            print(f"[notifications] Discord send failed: {e}")

    def _send_email(self, event: Dict[str, Any], message: str):
        # Build a short email
        subject = f"SIEM Alert: {event.get('type', 'alert')}"
        msg = MIMEText(message)
        msg["Subject"] = subject
        msg["From"] = self.email_from
        msg["To"] = self.email_to

        try:
            port = int(self.smtp_port) if self.smtp_port else 465
            # use SMTP_SSL if typical 465, otherwise try STARTTLS if port 587
            if port == 465:
                server = smtplib.SMTP_SSL(self.smtp_server, port, timeout=10)
                server.login(self.smtp_user, self.smtp_password)
            else:
                server = smtplib.SMTP(self.smtp_server, port, timeout=10)
                server.ehlo()
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
            server.sendmail(self.email_from, [self.email_to], msg.as_string())
            server.quit()
        except Exception as e:
            print(f"[notifications] Email send failed: {e}")
