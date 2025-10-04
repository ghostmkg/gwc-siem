import sys
from datetime import datetime
from app.parsers import parse_auth_line, parse_nginx_line
from app.detectors import process_event
from app.storage import init_db, save_event

def main(file_path):
    init_db()
    count = 0
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line: continue
            parsed = parse_auth_line(line) or parse_nginx_line(line) or {
                "timestamp": datetime.utcnow(), "source": "unknown", "raw": line, "type": "unknown"
            }
            save_event(parsed["timestamp"], parsed["source"], parsed["raw"], parsed.get("type"))
            process_event(parsed)
            count += 1
    print(f"Parsed {count} lines from {file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python cli.py <path_to_log_file>")
        exit(1)
    main(sys.argv[1])
