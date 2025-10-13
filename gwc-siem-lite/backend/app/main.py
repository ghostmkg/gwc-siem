
from fastapi import FastAPI, UploadFile, File, HTTPException
from . import parser, detector, db, models

app = FastAPI()

@app.on_event("startup")
def startup_event():
    db.init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(file: UploadFile = File(...), kind: str = "auth"):
    try:
        parser_instance = parser.get_parser(kind)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    content = await file.read()
    lines = content.decode("utf-8").splitlines()

    events = []
    for line in lines:
        event = parser_instance.parse(line)
        if event:
            events.append(event)

    brute_force_detector = detector.BruteForceDetector()
    http_5xx_detector = detector.Http5xxBurstDetector()

    alerts = brute_force_detector.detect(events)
    alerts.extend(http_5xx_detector.detect(events))

    for alert in alerts:
        db.add_alert(alert)

    return {"message": f"Ingested and analyzed {len(lines)} lines. Found {len(alerts)} alerts."}

@app.get("/alerts", response_model=list[models.Alert])
def get_alerts(limit: int = 100):
    return db.get_alerts(limit=limit)
