# 🛡️ GWC-SIEM: Mini SIEM for Home Labs & Hacktoberfest

GWC-SIEM is a lightweight Security Information and Event Management (SIEM) tool designed for home labs, learning, and Hacktoberfest contributions. It parses common logs, detects simple security events like SSH brute-force attacks and HTTP 5xx bursts, stores alerts in SQLite, and exposes them via **FastAPI API**, CLI, and a lightweight dashboard.

---

## ✨ Features

- **Log Ingestion**  
  Upload `auth.log` or Nginx access logs via **API** or **UI**.

- **Parsers**  
  Convert raw log lines into structured `Event` objects for processing.

- **Detections**  
  - SSH brute-force attempts (sliding-window threshold detection).  
  - HTTP 5xx bursts (thresholds configurable via YAML).  

- **Storage**  
  SQLite database for simple, portable storage of alerts and events.

- **Dashboard**  
  Static HTML + JS dashboard that fetches alerts from the API.

- **CLI**  
  Batch scanning for local logs or offline use.

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```powershell
git clone https://github.com/<your-username>/gwc-siem.git
cd gwc-siem
