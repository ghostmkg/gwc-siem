
import re
from datetime import datetime

# Common Log Format: 127.0.0.1 - - [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326
APACHE_LOG_REGEX = re.compile(r'^(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>.*?)\] "(?P<method>\S+) (?P<url>\S+) .*?" (?P<status>\d{3}) (?P<size>\S+)')

def parse_apache_log(log_line: str) -> dict | None:
    """
    Parses a single line of an Apache access log in the common log format.
    """
    match = APACHE_LOG_REGEX.match(log_line)
    if not match:
        return None

    data = match.groupdict()
    
    # Convert timestamp to datetime object
    try:
        # Example timestamp: 10/Oct/2000:13:55:36 -0700
        data['timestamp'] = datetime.strptime(data['timestamp'], '%d/%b/%Y:%H:%M:%S %z')
    except ValueError:
        # Handle cases where the timestamp format is different
        return None
        
    # Convert status to int
    data['status'] = int(data['status'])
    
    # Convert size to int, handling '-' for no size
    if data['size'] == '-':
        data['size'] = 0
    else:
        data['size'] = int(data['size'])

    return data
