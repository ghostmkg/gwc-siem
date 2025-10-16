from pydantic import BaseModel
from datetime import datetime

class Event(BaseModel):
    timestamp: datetime
    source_ip: str
    message: str
    raw_log: str

class Alert(BaseModel):
    timestamp: datetime
    rule_name: str
    description: str
    source_ip: str
