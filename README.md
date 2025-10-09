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

```
Mini-SIEM/
├── app/
│   ├── main.py          # FastAPI application
│   ├── models.py        # Database models
│   ├── parsers.py       # Log parsing logic
│   ├── detectors.py     # Threat detection rules
│   ├── storage.py       # Database operations
│   └── static/          # Web dashboard
├── config/
│   ├── default.yaml     # Default configuration
│   └── detections.yaml  # Detection rules
├── tests/               # Test suite
└── requirements.txt     # Dependencies
```

### 🔧 Core Components

- **Log Parser**: Extracts structured data from raw log files
- **Threat Detector**: Analyzes events and generates alerts
- **Storage Engine**: Persists events and alerts in SQLite database
- **Web API**: RESTful API for log ingestion and alert retrieval
- **Dashboard**: Web interface for monitoring and analysis

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

## 📢 Join Our Community

Be a part of our growing community and stay connected! 🚀

<div align="center">

[![Discord](https://img.shields.io/badge/Discord-Join%20Us-7289da?style=for-the-badge&logo=discord)](https://discord.gg/YMJp48qbwR)
[![Telegram](https://img.shields.io/badge/Telegram-Join%20Chat-0088cc?style=for-the-badge&logo=telegram)](https://t.me/gwcacademy)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Follow%20Us-0077b5?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/company/gwc-academy/)

</div>

---

## ☕ Support the Project
<p>If you like this project and want to support future development, consider buying me a coffee:</p><br>
<a href="https://www.buymeacoffee.com/mgoshwami1c"> <img align="left" src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" height="50" width="210" alt="mgoshwami1c" ></a>
  
  <br><br/>
# 🛡️ Mini-SIEM — Lightweight Security Monitoring for Home Labs

A minimal SIEM (Security Information and Event Management) system for home labs and learning. It parses common system and web server logs, detects simple security events, stores alerts in SQLite, and exposes them via a **FastAPI REST API**, **CLI**, and **web dashboard**.

Perfect for:
- Homelab defenders 🧑‍💻
- Cybersecurity learners
- Hacktoberfest contributors 🎃

---

## ✨ Features

- ✅ Log parsing for:
  - `/var/log/auth.log` (SSH auth)
  - Nginx access/error logs
- 🔍 Detects:
  - SSH brute force attempts
  - Bursts of HTTP 5xx errors
- 💾 Stores alerts in local **SQLite**
- 🧪 REST API via **FastAPI**
- 🔧 Interactive CLI for querying
- 📊 Lightweight dashboard (HTML/JS)
- 🐳 Dockerized & pluggable

---

## 🚀 Quick Start

### 📦 Requirements

- Python 3.9+
- pip / virtualenv
- (optional) Docker

### ⚙️ Local Setup

```bash
g
