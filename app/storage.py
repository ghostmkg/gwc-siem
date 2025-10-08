from sqlmodel import SQLModel, Session, create_engine, select
from datetime import datetime
from typing import List
from app.models import Event, Alert

DATABASE_URL = "sqlite:///./mini_siem.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

def init_db():
    SQLModel.metadata.create_all(engine)

def save_event(timestamp: datetime, source: str, raw: str, event_type: str = None) -> Event:
    with Session(engine) as session:
        ev = Event(timestamp=timestamp, source=source, raw=raw, event_type=event_type)
        session.add(ev)
        session.commit()
        session.refresh(ev)
        return ev

def save_alert(timestamp: datetime, source: str, alert_type: str, details: str = None) -> Alert:
    with Session(engine) as session:
        a = Alert(timestamp=timestamp, source=source, alert_type=alert_type, details=details)
        session.add(a)
        session.commit()
        session.refresh(a)
        return a

def list_alerts(limit: int = 100) -> List[Alert]:
    with Session(engine) as session:
        q = select(Alert).order_by(Alert.timestamp.desc()).limit(limit)
        return session.exec(q).all()
