
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import timedelta
from .models import Event, Alert

class BaseDetector(ABC):
    @abstractmethod
    def detect(self, events: list[Event]) -> list[Alert]:
        pass

class BruteForceDetector(BaseDetector):
    def detect(self, events: list[Event]) -> list[Alert]:
        alerts = []
        failed_logins = defaultdict(list)
        for event in events:
            if event.message == "Failed SSH login":
                failed_logins[event.source_ip].append(event.timestamp)
        
        for ip, timestamps in failed_logins.items():
            if len(timestamps) >= 5:
                timestamps.sort()
                if timestamps[-1] - timestamps[0] < timedelta(minutes=1):
                    alerts.append(Alert(
                        timestamp=timestamps[-1],
                        rule_name="SSH Brute Force",
                        description=f"{len(timestamps)} failed logins from {ip} in 1 minute",
                        source_ip=ip
                    ))
        return alerts

class Http5xxBurstDetector(BaseDetector):
    def detect(self, events: list[Event]) -> list[Alert]:
        alerts = []
        http_errors = defaultdict(list)
        for event in events:
            if event.message.startswith("HTTP 5"):
                http_errors[event.source_ip].append(event.timestamp)

        for ip, timestamps in http_errors.items():
            if len(timestamps) >= 10:
                timestamps.sort()
                if timestamps[-1] - timestamps[0] < timedelta(minutes=5):
                    alerts.append(Alert(
                        timestamp=timestamps[-1],
                        rule_name="HTTP 5xx Burst",
                        description=f"{len(timestamps)} HTTP 5xx errors from {ip} in 5 minutes",
                        source_ip=ip
                    ))
        return alerts

class GeoIPBlocklistDetector(BaseDetector):
    # In a real-world scenario, this would be loaded from a file or a feed.
    BLOCKLIST = {"1.2.3.4", "5.6.7.8", "9.10.11.12"}

    def detect(self, events: list[Event]) -> list[Alert]:
        alerts = []
        for event in events:
            if event.source_ip in self.BLOCKLIST:
                alerts.append(Alert(
                    timestamp=event.timestamp,
                    rule_name="GeoIP Blocklist",
                    description=f"Traffic from blocklisted IP {event.source_ip}",
                    source_ip=event.source_ip
                ))
        return alerts
