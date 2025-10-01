# 🛠 LogMonitor — Lightweight Log Ingestion & Detection

**LogMonitor** is an open-source tool for ingesting, parsing, detecting, and visualizing suspicious activity from logs.  
It’s designed to be **portable, configurable, and easy to extend**, making it ideal for beginners and advanced users alike.

---

## 📥 Features

### 1. Log Ingestion
- Upload **auth.log** or **Nginx access logs** via **API** or **UI**.  
- Supports batch uploads for offline analysis.  

### 2. Parsers
- Converts raw log lines into structured **Event objects**.  
- Easily extendable to support new log formats.  

### 3. Detections
- **Sliding-window brute-force detection**: catch repeated failed login attempts.  
- **5xx-burst detection**: detect sudden spikes in server errors.  
- Thresholds configurable in a **YAML** file.  

### 4. Storage
- Uses **SQLite** for portability and simplicity.  
- Optionally extendable to PostgreSQL or other DBs.  

### 5. Dashboard
- Static **HTML + JS** dashboard that fetches alerts from the API.  
- Visualize detections, brute-force attempts, and 5xx bursts in real-time.  

### 6. CLI Tool
- Run **local batch scans** for sample logs or offline use.  
- Lightweight and scriptable.

---

## 🛠 Tech Stack (Suggested)
- **Backend/API:** Python (FastAPI / Flask) or Node.js  
- **Database:** SQLite (default), PostgreSQL optional  
- **Frontend Dashboard:** Static HTML + JS  
- **CLI:** Python or Node.js scripts  

---

## ⚙ Configuration Example (YAML)
```yaml
bruteforce:
  window_seconds: 60
  threshold: 5

http_errors:
  window_seconds: 120
  threshold: 10

// modify thresholds according To You....
