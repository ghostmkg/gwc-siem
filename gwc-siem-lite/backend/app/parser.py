
from abc import ABC, abstractmethod
import re
from datetime import datetime
from .models import Event

class BaseParser(ABC):
    @abstractmethod
    def parse(self, line: str) -> Event | None:
        pass

class AuthParser(BaseParser):
    def parse(self, line: str) -> Event | None:
        match = re.search(r"(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}).*sshd.*Failed password for.*from\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", line)
        if match:
            timestamp_str, source_ip = match.groups()
            timestamp = datetime.strptime(timestamp_str, "%b %d %H:%M:%S")
            return Event(timestamp=timestamp, source_ip=source_ip, message="Failed SSH login", raw_log=line)
        return None

class NginxParser(BaseParser):
    def parse(self, line: str) -> Event | None:
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] ".*" (\d{3})', line)
        if match:
            source_ip, timestamp_str, status_code = match.groups()
            timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
            if status_code.startswith("5"):
                return Event(timestamp=timestamp, source_ip=source_ip, message=f"HTTP {status_code}", raw_log=line)
        return None

class ApacheParser(BaseParser):
    def parse(self, line: str) -> Event | None:
        match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - - \[(.*?)\] ".*" (\d{3})', line)
        if match:
            source_ip, timestamp_str, status_code = match.groups()
            timestamp = datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
            return Event(timestamp=timestamp, source_ip=source_ip, message=f"HTTP {status_code}", raw_log=line)
        return None

def get_parser(kind: str) -> BaseParser:
    if kind == "auth":
        return AuthParser()
    elif kind == "nginx":
        return NginxParser()
    elif kind == "apache":
        return ApacheParser()
    raise ValueError(f"Unknown parser kind: {kind}")
