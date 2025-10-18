# 🛡️ Mini-SIEM - Security Information and Event Management System

<div align="center">

![Mini-SIEM](https://img.shields.io/badge/Mini--SIEM-Security%20Monitoring-red?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Web%20API-green?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

</div>

## 📌 Overview

**Mini-SIEM** is a lightweight Security Information and Event Management system designed for small to medium-sized organizations. It provides real-time log analysis, threat detection, and security alerting capabilities.

### 🎯 Key Features

- **📊 Log Ingestion**: Parse and process various log formats (SSH, Nginx, Apache)
- **🚨 Threat Detection**: Real-time detection of security threats and anomalies
- **📈 Alerting System**: Generate alerts for suspicious activities
- **🌐 Web Dashboard**: User-friendly interface for monitoring and analysis
- **🔍 Event Analysis**: Comprehensive event parsing and correlation
- **⚡ Real-time Processing**: Fast log processing with configurable thresholds

---

## 🏗️ Architecture

* **Log ingestion:** Upload `auth.log` or Nginx access logs via API or UI
* **Parsers:** Convert raw lines → structured `Event` objects
* **Detections:** Sliding-window brute-force & 5xx-burst rules (thresholds configurable in YAML)
* **Storage:** SQLite for easy portability
* **Dashboard:** Static HTML + JS fetch alerts from API
* **CLI:** Local batch scanning for sample logs or offline use

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1️⃣ Installation

```bash
# Clone the repository
git clone https://github.com/ghostmkg/gwc-siem.git
cd gwc-siem

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configuration

The system uses YAML configuration files for detection rules:

```yaml
# config/detections.yaml
detectors:
  ssh_bruteforce:
    window_seconds: 300    # 5 minutes
    attempts_threshold: 5  # 5 failed attempts
    
  http_5xx_burst:
    window_seconds: 60     # 1 minute
    errors_threshold: 10   # 10 server errors
```

### 3️⃣ Running the Application

```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **Dashboard**: http://localhost:8000/static/index.html
- **API Documentation**: http://localhost:8000/docs

---

## 📖 Usage

### 📤 Log Ingestion

Upload log files via the `/ingest` endpoint:

```bash
# Upload SSH auth log
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@/var/log/auth.log" \
  -F "source=ssh_server"

# Upload Nginx access log
curl -X POST "http://localhost:8000/ingest" \
  -F "file=@/var/log/nginx/access.log" \
  -F "source=web_server"
```

### 🚨 Alert Retrieval

Get recent security alerts:

```bash
# Get latest 50 alerts
curl "http://localhost:8000/alerts?limit=50"
```

### 📊 Dashboard

Access the web dashboard at `/static/index.html` for:
- Real-time event monitoring
- Alert visualization
- Security metrics
- Log analysis tools

---

## 🔍 Supported Log Formats

### SSH Authentication Logs

```
Jan 15 10:30:45 server sshd[1234]: Failed password for root from 192.168.1.100
Jan 15 10:30:50 server sshd[1235]: Accepted password for admin from 192.168.1.101
```

**Detected Events:**
- `ssh.failed_password`: Failed login attempts
- `ssh.login_success`: Successful logins
- `auth.other`: Other authentication events

### Nginx Access Logs

```
192.168.1.100 - - [15/Jan/2024:10:30:45 +0000] "GET /admin HTTP/1.1" 404 123 "-" "Mozilla/5.0"
192.168.1.101 - - [15/Jan/2024:10:30:50 +0000] "POST /login HTTP/1.1" 200 456 "-" "Mozilla/5.0"
```

**Detected Events:**
- `nginx.access`: HTTP requests with status codes
- Server error detection (5xx responses)
- Request pattern analysis

---

## 🚨 Threat Detection

### Current Detectors

1. **SSH Brute Force Detection**
   - Monitors failed password attempts
   - Configurable threshold and time window
   - Generates alerts for suspicious activity

2. **HTTP 5xx Error Burst Detection**
   - Detects server error spikes
   - Identifies potential DoS attacks
   - Monitors web server health

### 🔧 Adding Custom Detectors

Create new detection rules in `app/detectors.py`:

```python
def process_event(parsed: Dict[str, Any]):
    # Your custom detection logic here
    if parsed.get("type") == "your_event_type":
        # Analyze the event
        if suspicious_condition:
            save_alert(
                timestamp=datetime.utcnow(),
                source=parsed.get("ip"),
                alert_type="custom_threat",
                details="Description of the threat"
            )
```

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
## 🧪 Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_detector.py

# Run with coverage
python -m pytest --cov=app tests/
```

### Test Data

The repository includes sample log files for testing:
- `nginx.log`: Sample Nginx access log
- Test scripts for validation

---

## 🐳 Docker Deployment

```bash
# Build Docker image
docker build -t mini-siem .

# Run container
docker run -p 8000:8000 mini-siem

# Using Docker Compose
docker-compose up -d
```

---

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API status and information |
| `/ingest` | POST | Upload and process log files |
| `/alerts` | GET | Retrieve security alerts |
| `/static/index.html` | GET | Web dashboard |

### API Examples

```python
import requests

# Upload log file
with open('auth.log', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/ingest',
        files={'file': f},
        data={'source': 'ssh_server'}
    )
    print(f"Parsed {response.json()['parsed_lines']} lines")

# Get alerts
alerts = requests.get('http://localhost:8000/alerts?limit=10')
for alert in alerts.json():
    print(f"Alert: {alert['alert_type']} from {alert['source']}")
```

🔔 Notifications Feature

The Notifications system alerts users in real-time when new security events or logs are ingested.

🧩 How to Run

1. Start the Flask server:
python -m api.ingest
The server runs on http://127.0.0.1:5000

2. Keep this server running in the background while you use the dashboard or API.

3. When new logs are uploaded or alerts are generated, notifications will appear automatically.

🧠 How It Works

-The api/ingest.py script listens for new events.
-Detected alerts trigger in-app notifications.
-Ideal for monitoring real-time ingestion and alert generation.
---

## 🔧 Configuration

### Environment Variables

```bash
# Database configuration
DATABASE_URL=sqlite:///mini_siem.db

# Logging level
LOG_LEVEL=INFO

# API settings
API_HOST=0.0.0.0
API_PORT=8000
```

### Detection Rules

Customize detection thresholds in `config/detections.yaml`:

```yaml
detectors:
  ssh_bruteforce:
    window_seconds: 300      # Time window for analysis
    attempts_threshold: 5    # Number of failed attempts
    
  http_5xx_burst:
    window_seconds: 60       # Time window for analysis
    errors_threshold: 10     # Number of server errors
```

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🐛 Reporting Issues

1. Check existing issues to avoid duplicates
2. Provide detailed information about the problem
3. Include steps to reproduce the issue

### 💻 Code Contributions

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Commit your changes (`git commit -m 'Add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

### 📝 Documentation

Help improve documentation by:
- Fixing typos and grammar
- Adding code examples
- Improving API documentation
- Writing tutorials

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test
pytest tests/test_detector.py::test_ssh_bruteforce
```

---

## 📋 Roadmap

- [x] Basic log parsing (SSH, Nginx)
- [x] Threat detection engine
- [x] Web dashboard
- [x] REST API
- [ ] Additional log formats (Apache, Windows Event Logs)
- [ ] Machine learning-based anomaly detection
- [ ] Email/Slack notifications
- [ ] Advanced correlation rules
- [ ] User authentication and authorization
- [ ] Data retention policies
- [ ] Performance optimization

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

---

## 📢 Join Our Community

Be a part of our growing community and stay connected 🚀

* 🗨️ [Join us on Discord](https://discord.gg/YMJp48qbwR)
* 📢 [Join our Telegram](https://t.me/gwcacademy)
* 💼 [Follow our LinkedIn Page](https://www.linkedin.com/company/gwc-academy/)
* 💬 [Join our WhatsApp Community](https://whatsapp.com/channel/0029ValnoT1CBtxNi4lt8h1s)
* 📺 [Subscribe on YouTube](https://www.youtube.com/c/growwithcode?sub_confirmation=1)
* 🐦 [Follow on Twitter](https://x.com/goshwami_manish)
* 📸 [Follow on Instagram](https://www.instagram.com/grow_with_code)

---

## ☕ Support the Project

If you like this project and want to support future development, consider buying me a coffee:

<a href="https://www.buymeacoffee.com/mgoshwami1c">
  <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="mgoshwami1c">
</a>

<br><br/>
