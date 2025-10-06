from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from app.parsers import parse_auth_line, parse_nginx_line
from app.storage import init_db, save_event, list_alerts
from app.detectors import process_event
from datetime import datetime
import io

app = FastAPI(title="Mini-SIEM")

# Serve static dashboard
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
def startup():
    # Initialize database
    init_db()

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), source: str = Form(None)):
    """
    Upload a log file (auth.log or nginx access log), parse line-by-line, run detectors.
    Returns count of parsed lines.
    """
    content = await file.read()
    text = content.decode(errors="ignore")
    parsed_count = 0

    for raw_line in io.StringIO(text):
        raw_line = raw_line.strip()
        if not raw_line:
            continue

        # Parse the line
        parsed = parse_auth_line(raw_line) or parse_nginx_line(raw_line) or {
            "timestamp": datetime.utcnow(),
            "source": source or file.filename,
            "raw": raw_line,
            "type": "unknown"
        }

        # Save event to DB
        save_event(parsed["timestamp"], parsed["source"], parsed["raw"], parsed.get("type"))

        # Run detectors to generate alerts if thresholds are met
        process_event(parsed)

        parsed_count += 1

    return {"parsed_lines": parsed_count}

@app.get("/alerts")
def get_alerts(limit: int = 100):
    """
    Fetch recent alerts (JSON).
    """
    return list_alerts(limit)

@app.get("/")
def index():
    """
    Root endpoint: points to dashboard.
    """
    return {"message": "Mini-SIEM API running. Dashboard available at /static/index.html"}
