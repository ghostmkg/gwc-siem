# 🛡️ Mini‑SIEM - Home Lab Security Event Monitor

**Mini‑SIEM** is a lightweight Security Information and Event Management system designed for **home labs** and Hacktoberfest contributors. It helps you **collect, parse, and analyze logs** from common sources, detect simple security events, and monitor them via a web API, CLI, or dashboard.

---

## ✨ Key Features

- **Log Parsing** → Supports common log types like `auth.log` and `nginx` access logs.  
- **Security Event Detection** → Detects simple events such as:
  - SSH brute-force attempts  
  - HTTP 5xx bursts  
- **Storage** → Uses **SQLite** for easy setup and portability.  
- **Access & Monitoring** → Exposes alerts via:
  - **FastAPI API**  
  - **Command-Line Interface (CLI)**  
  - **Lightweight HTML/JS dashboard**  
- **Configurable Thresholds** → Easily tweak detection rules via YAML files.

---

## 🎯 Why Mini‑SIEM?

Home labs often lack the **full-featured SIEM tools** used in enterprises. Mini‑SIEM provides a **simple, practical solution** for learning, monitoring, and contributing to open source security projects:

- Learn **log analysis and alerting** in a hands-on environment.  
- Experiment with **detection rules** and security monitoring.  
- Contribute easily for **Hacktoberfest** by adding parsers, detection rules, or dashboard features.

---

## 🛠️ How It Works

1. **Log Ingestion** → Upload `auth.log` or `nginx` logs via API or CLI.  
2. **Parsing & Event Detection** → Converts raw logs into structured events and checks for alerts.  
3. **Storage** → Saves events and alerts in **SQLite**.  
4. **Access Alerts** → Query alerts via:
   - **FastAPI endpoints**  
   - **CLI commands**  
   - **Web dashboard**  

---

## 🚀 Ideal For

- Home lab enthusiasts learning **SIEM basics**.  
- Hacktoberfest contributors wanting **practical security projects**.  
- Students or hobbyists experimenting with **log analysis and detection**.

---

## 🌍 Vision

Mini‑SIEM aims to **bring enterprise-level concepts to personal labs** in a lightweight, accessible way. By combining log parsing, event detection, storage, and dashboards in a single project, it becomes a **perfect playground for learning and contributing** to security monitoring tools.
