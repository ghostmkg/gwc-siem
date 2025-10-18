
import re
from datetime import datetime

# Oct 10 13:55:36 server-name sshd[12345]: Failed password for invalid user user from 127.0.0.1 port 12345 ssh2
AUTH_LOG_REGEX = re.compile(r'^(?P<timestamp>\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})\s+\S+\s+(?P<process>\w+)\[\d+\]: (?P<message>.*)$')

def parse_auth_log(log_line: str) -> dict | None:
    """
    Parses a single line of an auth.log file.
    """
    match = AUTH_LOG_REGEX.match(log_line)
    if not match:
        return None

    data = match.groupdict()
    
    # Convert timestamp to datetime object
    try:
        # Example timestamp: Oct 10 13:55:36
        data['timestamp'] = datetime.strptime(data['timestamp'], '%b %d %H:%M:%S')
        # Add current year to the timestamp
        data['timestamp'] = data['timestamp'].replace(year=datetime.now().year)
    except ValueError:
        # Handle cases where the timestamp format is different
        return None

    return data
