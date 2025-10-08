import re
from datetime import datetime
from typing import Optional, Dict

# auth.log
_auth_re = re.compile(r"(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<host>\S+)\s+(?P<proc>sshd\[\d+\]):\s+(?P<msg>.*)")
_failed_pw_re = re.compile(r"Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)")
_accepted_pw_re = re.compile(r"Accepted password for (?P<user>\S+) from (?P<ip>\d+\.\d+\.\d+\.\d+)")

MONTHS = {'Jan':1,'Feb':2,'Mar':3,'Apr':4,'May':5,'Jun':6,'Jul':7,'Aug':8,'Sep':9,'Oct':10,'Nov':11,'Dec':12}

def parse_syslog_timestamp(month:str, day:str, timestr:str) -> datetime:
    now = datetime.utcnow()
    month_n = MONTHS.get(month, now.month)
    year = now.year
    return datetime.strptime(f"{year}-{month_n}-{day} {timestr}", "%Y-%m-%d %H:%M:%S")

def parse_auth_line(line: str) -> Optional[Dict]:
    m = _auth_re.match(line)
    if not m: return None
    msg = m.group("msg")
    timestamp = parse_syslog_timestamp(m.group("month"), m.group("day"), m.group("time"))
    failed = _failed_pw_re.search(msg)
    if failed:
        return {"timestamp": timestamp, "source": m.group("host"), "raw": line.strip(), "type": "ssh.failed_password",
                "ip": failed.group("ip"), "user": failed.group("user"), "success": False}
    accepted = _accepted_pw_re.search(msg)
    if accepted:
        return {"timestamp": timestamp, "source": m.group("host"), "raw": line.strip(), "type": "ssh.login_success",
                "ip": accepted.group("ip"), "user": accepted.group("user"), "success": True}
    return {"timestamp": timestamp, "source": m.group("host"), "raw": line.strip(), "type": "auth.other", "msg": msg}

# nginx access log
_nginx_re = re.compile(
    r'(?P<ip>\d+\.\d+\.\d+\.\d+)\s+\S+\s+\S+\s+\[(?P<time>[^\]]+)\]\s+"(?P<method>\S+)\s+(?P<path>\S+)[^"]*"\s+(?P<status>\d{3})\s+(?P<size>\d+)\s+"(?P<ref>[^"]*)"\s+"(?P<ua>[^"]*)"'
)
def parse_nginx_time(timestr: str) -> datetime:
    dt = datetime.strptime(timestr.split()[0], "%d/%b/%Y:%H:%M:%S")
    return dt

def parse_nginx_line(line: str) -> Optional[Dict]:
    m = _nginx_re.match(line)
    if not m: return None
    status = int(m.group("status"))
    ts = parse_nginx_time(m.group("time"))
    return {"timestamp": ts, "source": "nginx", "raw": line.strip(), "type": "nginx.access",
            "ip": m.group("ip"), "method": m.group("method"), "path": m.group("path"), "status": status}
