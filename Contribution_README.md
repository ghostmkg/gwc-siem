# 🛡️ Mini-SIEM

**Mini-SIEM** is a lightweight Security Information and Event Management system for **home labs** and **Hacktoberfest contributions**.  
It parses common logs (auth, nginx), detects simple security events (SSH brute force, HTTP 5xx bursts), stores alerts in SQLite, and exposes them via **FastAPI API**, **CLI**, and a **lightweight dashboard**.

---

## 🌟 Features

- Parse common logs:
  - `/var/log/auth.log` → detect SSH brute force attempts  
  - `nginx/access.log` → detect HTTP 5xx bursts
- Store alerts in **SQLite** (`alerts.db`)
- Expose alerts via:
  - **FastAPI API** (`/alerts`)  
  - **CLI** to manually scan logs  
  - **Lightweight Dashboard** (HTML/JS)
- Beginner-friendly and modular — perfect for Hacktoberfest

---

## 🛠 Tech Stack

- **Backend:** Python + FastAPI  
- **Database:** SQLite  
- **CLI:** Python  
- **Dashboard:** HTML, CSS, JavaScript  

---

## 📂 Folder Structure

mini-siem/ ├── backend/ │   ├── app/ │   │   ├── main.py │   │   ├── parser.py │   │   ├── detector.py │   │   ├── db.py │   │   └── models.py │   └── requirements.txt ├── cli/ │   └── siem_cli.py ├── dashboard/ │   └── index.html └──
