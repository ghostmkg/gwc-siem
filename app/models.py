from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Event(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    source: Optional[str] = None
    raw: str
    event_type: Optional[str] = None

class Alert(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    timestamp: datetime
    source: Optional[str] = None
    alert_type: str
    details: Optional[str] = None
