
import sqlite3
from .models import Alert

DATABASE = "alerts.db"

def init_db():
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                rule_name TEXT NOT NULL,
                description TEXT NOT NULL,
                source_ip TEXT NOT NULL
            )
        """)
        con.commit()

def add_alert(alert: Alert):
    with sqlite3.connect(DATABASE) as con:
        cur = con.cursor()
        cur.execute("INSERT INTO alerts (timestamp, rule_name, description, source_ip) VALUES (?, ?, ?, ?)",
                    (alert.timestamp.isoformat(), alert.rule_name, alert.description, alert.source_ip))
        con.commit()

def get_alerts(limit: int = 100) -> list[Alert]:
    with sqlite3.connect(DATABASE) as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cur.fetchall()
        return [Alert(**row) for row in rows]
