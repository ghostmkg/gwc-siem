from collections import deque, defaultdict
from datetime import datetime, timedelta
from typing import Dict, Any
from .storage import save_alert
import yaml, os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.yaml")
with open(CONFIG_PATH) as f:
    config = yaml.safe_load(f)

ssh_failures: Dict[str, deque] = defaultdict(deque)
http_5xx: Dict[str, deque] = defaultdict(deque)

def _trim_deque(d: deque, window_seconds: int):
    now = datetime.utcnow()
    cutoff = now - timedelta(seconds=window_seconds)
    while d and d[0] < cutoff:
        d.popleft()

def process_event(parsed: Dict[str, Any]):
    now = datetime.utcnow()
    # SSH
    if parsed.get("type") == "ssh.failed_password":
        ip = parsed.get("ip") or parsed.get("source")
        cfg = config["detectors"]["ssh_bruteforce"]
        dq = ssh_failures[ip]
        dq.append(parsed.get("timestamp", now))
        _trim_deque(dq, cfg["window_seconds"])
        if len(dq) >= cfg["attempts_threshold"]:
            save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="ssh_bruteforce",
                       details=f"{len(dq)} failed SSH attempts")
            dq.clear()
    # HTTP 5xx
    if parsed.get("type") == "nginx.access":
        status = int(parsed.get("status", 0))
        ip = parsed.get("ip", "unknown")
        if 500 <= status <= 599:
            cfg = config["detectors"]["http_5xx_burst"]
            dq = http_5xx[ip]
            dq.append(parsed.get("timestamp", now))
            _trim_deque(dq, cfg["window_seconds"])
            if len(dq) >= cfg["errors_threshold"]:
                save_alert(timestamp=datetime.utcnow(), source=ip, alert_type="http_5xx_burst",
                           details=f"{len(dq)} HTTP 5xx responses")
                dq.clear()
