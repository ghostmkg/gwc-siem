# notifications/hooks.py
"""
Lightweight hook to import and call from detection modules.
Place one line in detection code where Alert objects/dicts are created:
    from notifications.hooks import handle_alert
    handle_alert(alert_dict)
This file loads config once and exposes a simple function.
"""
from typing import Dict, Any
import os

from .sender import NotificationManager

# Singleton manager
_MANAGER = None

def _get_manager() -> NotificationManager:
    global _MANAGER
    if _MANAGER is not None:
        return _MANAGER

    # prefer repo config file, fallback to env vars
    cfg_path = os.environ.get("SIEM_CONFIG_PATH", "config/config.json")
    _MANAGER = NotificationManager.from_config(cfg_path)
    return _MANAGER

def handle_alert(event: Dict[str, Any]) -> None:
    """
    Top-level hook to call from detection code.
    Accepts a dict-like event. Example:
      {
        "type": "ssh_brute_force",
        "source_ip": "1.2.3.4",
        "timestamp": "2025-10-18T08:00:00Z",
        "count": 10,
        "raw": "...original log line..."
      }
    """
    if not isinstance(event, dict):
        # make a best effort to convert
        try:
            event = dict(event)
        except Exception:
            return
    manager = _get_manager()
    # non-blocking send with internal rate-limiter
    manager.notify(event)

import traceback
print("[notifications] failed to handle alert:")
traceback.print_exc()
