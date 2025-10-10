<img width="1536" height="1024" alt="ChatGPT Image Sep 29, 2025, 02_16_49 AM" src="https://github.com/user-attachments/assets/17e7065e-791d-473f-9066-cdbde083e32e" />

# gwc-siem 🛡️

A **mini‑SIEM** for home labs and Hacktoberfest contributions. Parses common logs (auth, nginx), detects simple security events (SSH brute force, HTTP 5xx bursts), stores alerts in SQLite, and exposes them via **FastAPI API**, **CLI**, and a **lightweight dashboard**.


---

## ✨ Features

* **Log ingestion:** Upload `auth.log` or Nginx access logs via API or UI
* **Parsers:** Convert raw lines → structured `Event` objects
* **Detections:** Sliding‑window brute‑force & 5xx‑burst rules (thresholds configurable in YAML)
* **Storage:** SQLite for easy portability
* **Dashboard:** Static HTML + JS fetch alerts from API
* **CLI:** Local batch scanning for sample logs or offline use

---

## 🚀 Quickstart

### 1. Clone & setup

```bash
git clone https://github.com/<your-username>/gwc-siem.git
cd gwc-siem-lite
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

### 2. Run API

```bash
uvicorn api.main:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Upload sample logs from `sample_data/` using the upload form. Alerts will appear in a table below.

### 3. Use CLI

```bash
python cli/app.py --file sample_data/auth.log --kind auth
```

This parses, detects alerts, and writes them to `seclog.db`. You can fetch them via API:

```bash
curl http://127.0.0.1:8000/alerts?limit=10 | jq
```

---

**Core components:**

* **API (`api/`)**: `/ingest`, `/alerts`, `/health`
* **Parsers (`core/parsers/`)**: auth + nginx → `Event`
* **Detections (`core/detections/`)**: brute_force + http_5xx_burst → `Alert`
* **Storage (`storage/`)**: SQLite + helper functions
* **Web (`web/index.html`)**: upload form + table renderer
* **CLI (`cli/`)**: batch scanning tool

---
### Request/Response Flow
- **API Endpoints:** 
  - `/ingest` → accepts logs for processing
  - `/alerts` → retrieves generated alerts
- **Web UI / CLI:** Interacts with the API to visualize and manage alerts.

### Extensibility
- Add new parsers or detection rules easily.
- Built to be **modular** and **lightweight**.

### Deployment
- Supports local deployment or containerization using Docker.

### Data Models
- **Event:** `timestamp`, `log line`
- **Alert:** `timestamp`, `source`, `type`

---
## 🧑‍💻 Contributing

1. Fork & clone repo
2. Create a branch for your change
3. Setup local env:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .
```

4. Run tests:

```bash
pytest -q
```

5. Open a PR referencing an issue (see [CONTRIBUTING.md](CONTRIBUTING.md))

---

## 📌 Roadmap

* [ ] Apache access log parser
* [ ] GeoIP blocklist rule
* [ ] Prometheus `/metrics` endpoint
* [ ] Docker Compose example with log mounts
* [ ] Alert notifiers (Slack, Discord)

---

## 🛡️ Security

See [SECURITY.md](SECURITY.md). For severe issues, disclose privately.

---



## 📄 License

MIT © 2025 ghostmkg

## 📢 Join Our Community
This project is open for everyone. Whether you are a beginner or experienced coder, you are welcome to contribute. Let’s learn and grow together! 🌱


Be a part of our growing community and stay connected 🚀  

- 🗨️ [Join us on Discord](https://discord.gg/YMJp48qbwR)
- 📢 [Join our Telegram](https://t.me/gwcacademy)
- 💼 [Follow our LinkedIn Page](https://www.linkedin.com/company/gwc-academy/)  
- 💬 [Join our WhatsApp Community](https://whatsapp.com/channel/0029ValnoT1CBtxNi4lt8h1s)
- 📺 [Subscribe on YouTube](https://www.youtube.com/c/growwithcode?sub_confirmation=1)  
- 🐦 [Follow on Twitter](https://x.com/goshwami_manish) 
- 📸 [Follow on Instagram](https://www.instagram.com/grow_with_code)  


## ☕ Support the Project
<p>If you like this project and want to support future development, consider buying me a coffee:</p><br>
<a href="https://www.buymeacoffee.com/mgoshwami1c"> <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="mgoshwami1c" ></a>
  
  <br><br/>
