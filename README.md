 Mini-SIEM

Mini-SIEM is a lightweight Security Information and Event Management tool built with FastAPI.  
It parses **auth.log** and **nginx access logs**, detects security events (SSH brute-force attempts, HTTP 5xx bursts), and shows alerts in a web dashboard.

---

## Features

- Parse SSH auth logs and nginx access logs
- Detect:
  - SSH brute-force attempts
  - HTTP 5xx bursts
- Store events and alerts in SQLite database
- Dashboard auto-refreshes to show latest alerts

---

## Prerequisites

- Python 3.10+
- Git (optional)

---

## Setup Instructions

### 1️⃣ Clone Project

```bash
git clone <your-repo-url>
cd gwc-siem
2️⃣ Create & Activate Virtual Environment
Windows:

bash
Copy code
python -m venv .venv
.venv\Scripts\activate
Linux / MacOS:

bash
Copy code
python3 -m venv .venv
source .venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
Usage
1️⃣ Parse a Log File via CLI
bash
Copy code
python cli.py "path\to\nginx.log"
Example:

bash
Copy code
python cli.py "C:\Users\KRUSHNALI\Downloads\nginx.log"
2️⃣ Start FastAPI Server
bash
Copy code
uvicorn main:app --reload
Visit dashboard: http://127.0.0.1:8000/static/index.html

API Endpoints:

POST /ingest → Upload a log file

GET /alerts → Fetch latest alerts

3️⃣ Deactivate Virtual Environment
bash
Copy code
deactivate
Configuration
app/config.yaml contains detector thresholds and parser options:

yaml
Copy code
detectors:
  ssh_bruteforce:
    attempts_threshold: 5
    window_seconds: 300

  http_5xx_burst:
    errors_threshold: 3
    window_seconds: 120

parsers:
  nginx:
    enabled: true
  auth:
    enabled: true
Update thresholds according to your needs.

Project Structure
arduino
Copy code
gwc-siem/
│
├─ app/
│  ├─ __init__.py
│  ├─ detectors.py
│  ├─ parsers.py
│  ├─ storage.py
│  ├─ models.py
│  └─ static/
│       ├─ index.html
│       └─ dashboard.js
├─ cli.py
├─ main.py
├─ config.yaml
├─ requirements.txt
└─ README.md