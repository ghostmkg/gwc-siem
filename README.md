<img width="1536" height="1024" alt="ChatGPT Image Sep 29, 2025, 02_16_49 AM" src="https://github.com/user-attachments/assets/17e7065e-791d-473f-9066-cdbde083e32e" />

# GWC-SIEM 🛡️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Hacktoberfest](https://img.shields.io/badge/Hacktoberfest-friendly-blueviolet)](https://hacktoberfest.digitalocean.com/)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)

A **lightweight Security Information and Event Management (SIEM)** system designed for home labs, educational purposes, and Hacktoberfest contributions. 

**GWC-SIEM** provides real-time log parsing, threat detection, and security alerting capabilities with a simple, extensible architecture that's perfect for learning cybersecurity concepts and building security monitoring skills.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Log Sources   │───▶│    GWC-SIEM      │───▶│    Outputs      │
│                 │    │                  │    │                 │
│ • Auth logs     │    │ ┌──────────────┐ │    │ • SQLite DB     │
│ • Nginx logs    │    │ │   Parsers    │ │    │ • REST API      │
│ • Apache logs   │    │ │              │ │    │ • Web Dashboard │
│ • Custom logs   │    │ └──────────────┘ │    │ • CLI Output    │
│                 │    │ ┌──────────────┐ │    │ • Alerts        │
└─────────────────┘    │ │  Detections  │ │    └─────────────────┘
                       │ │              │ │
                       │ └──────────────┘ │
                       │ ┌──────────────┐ │
                       │ │   Storage    │ │
                       │ │              │ │
                       │ └──────────────┘ │
                       └──────────────────┘
```

---

## ✨ Features

### 🔍 **Log Processing**
* **Multi-format Support**: Auth logs, Nginx access logs, Apache logs (planned)
* **Real-time Ingestion**: Upload via API, CLI batch processing, or file monitoring
* **Structured Parsing**: Convert raw log lines into structured `Event` objects
* **Custom Parsers**: Extensible parser framework for new log formats

### 🚨 **Threat Detection**
* **Brute Force Detection**: SSH/FTP login attempt monitoring with configurable thresholds
* **HTTP Anomaly Detection**: 5xx error burst detection and rate limiting violations
* **Custom Rules**: YAML-based detection rule configuration
* **Sliding Window Analysis**: Time-based threat pattern recognition

### 💾 **Data Management**
* **SQLite Storage**: Lightweight, portable database for events and alerts
* **Event Correlation**: Link related security events across time windows
* **Data Retention**: Configurable retention policies for log data
* **Export Capabilities**: JSON/CSV export for further analysis

### 🌐 **User Interfaces**
* **REST API**: Full-featured FastAPI with OpenAPI documentation
* **Web Dashboard**: Lightweight HTML5 dashboard for alert monitoring
* **CLI Tool**: Command-line interface for batch processing and automation
* **API Documentation**: Interactive Swagger UI at `/docs`

### ⚡ **Performance & Scalability**
* **Asynchronous Processing**: FastAPI with async/await support
* **Configurable Thresholds**: Tune detection sensitivity via YAML config
* **Resource Efficient**: Minimal memory footprint for home lab deployment
* **Extensible Architecture**: Plugin-ready design for custom components

---

## 🚀 Quick Start Guide

### Prerequisites
- **Python 3.8+** 
- **Git**
- **Virtual Environment** (recommended)

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/Shubham11440/gwc-siem.git
cd gwc-siem

# Create and activate virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate.bat
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -e .
```

### 2. Configuration

Create a configuration file:

```bash
# Copy default configuration
cp config/default.yaml config/local.yaml

# Edit configuration as needed
# notepad config/local.yaml  # Windows
# nano config/local.yaml     # Linux/macOS
```

### 3. Start the API Server

```bash
# Development mode with hot reload
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# Production mode
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

**🌐 Access Points:**
- **Web Dashboard**: [http://localhost:8000](http://localhost:8000)
- **API Documentation**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

### 4. Test with Sample Data

```bash
# Upload sample auth logs
curl -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@sample_data/auth.log" \
  -F "log_type=auth"

# Check for generated alerts
curl "http://localhost:8000/alerts?limit=10" | jq '.'

# View events
curl "http://localhost:8000/events?limit=20" | jq '.'
```

### 5. CLI Usage

```bash
# Process auth logs
python cli/app.py --file sample_data/auth.log --kind auth

# Process nginx logs
python cli/app.py --file sample_data/access.log --kind nginx

# Generate sample data for testing
python cli/app.py --generate-sample --output sample_auth.log
```

## 📁 Project Structure

```
gwc-siem/
├── 📁 api/                    # FastAPI application
│   ├── main.py               # API entry point
│   ├── routes/               # API route definitions
│   └── models/               # Pydantic models
├── 📁 core/                   # Core SIEM functionality
│   ├── parsers/              # Log format parsers
│   │   ├── auth.py          # Auth log parser
│   │   ├── nginx.py         # Nginx log parser
│   │   └── base.py          # Base parser class
│   ├── detections/           # Threat detection rules
│   │   ├── brute_force.py   # SSH/FTP brute force detection
│   │   ├── http_anomaly.py  # HTTP error burst detection
│   │   └── base.py          # Base detection class
│   └── models/               # Data models
│       ├── event.py         # Event data structure
│       └── alert.py         # Alert data structure
├── 📁 storage/                # Data persistence layer
│   ├── database.py          # SQLite operations
│   ├── models.py            # Database schema
│   └── migrations/          # Database migrations
├── 📁 web/                    # Frontend dashboard
│   ├── index.html           # Main dashboard
│   ├── static/              # CSS/JS assets
│   └── templates/           # HTML templates
├── 📁 cli/                    # Command-line interface
│   ├── app.py               # CLI application
│   └── commands/            # CLI command modules
├── 📁 config/                 # Configuration files
│   ├── default.yaml         # Default configuration
│   └── detections.yaml      # Detection rules config
├── 📁 sample_data/            # Sample log files for testing
│   ├── auth.log             # Sample auth logs
│   ├── nginx.log            # Sample nginx logs
│   └── malicious.log        # Sample attack logs
├── 📁 tests/                  # Test suite
│   ├── unit/                # Unit tests
│   ├── integration/         # Integration tests
│   └── fixtures/            # Test data fixtures
├── 📁 docs/                   # Documentation
│   ├── api/                 # API documentation
│   ├── deployment/          # Deployment guides
│   └── examples/            # Usage examples
├── 📄 requirements.txt        # Python dependencies
├── 📄 requirements-dev.txt    # Development dependencies
├── 📄 setup.py               # Package setup
├── 📄 .env.example           # Environment variables template
├── 📄 docker-compose.yml     # Docker deployment
└── 📄 Dockerfile             # Container definition
```

---

## 🔧 API Documentation

### Core Endpoints

| Method | Endpoint | Description | Parameters |
|--------|----------|-------------|------------|
| `POST` | `/ingest` | Upload and process log files | `file`, `log_type` |
| `GET` | `/alerts` | Retrieve security alerts | `limit`, `offset`, `severity` |
| `GET` | `/events` | Retrieve parsed events | `limit`, `offset`, `event_type` |
| `GET` | `/health` | System health check | None |
| `GET` | `/stats` | System statistics | `timeframe` |

### Alert Endpoints

```bash
# Get recent alerts
GET /alerts?limit=50&severity=high

# Get alerts by time range
GET /alerts?start_time=2025-01-01T00:00:00Z&end_time=2025-01-02T00:00:00Z

# Get alert details
GET /alerts/{alert_id}

# Acknowledge alert
PATCH /alerts/{alert_id}/acknowledge
```

### Event Endpoints

```bash
# Get events by type
GET /events?event_type=authentication&limit=100

# Get events by source IP
GET /events?source_ip=192.168.1.100

# Export events as CSV
GET /events/export?format=csv&start_time=2025-01-01T00:00:00Z
```

---

## ⚙️ Configuration

### Detection Rules (`config/detections.yaml`)

```yaml
brute_force:
  enabled: true
  window_seconds: 300        # 5-minute window
  threshold: 5               # 5 failed attempts
  sources:
    - ssh
    - ftp
    - http_auth

http_anomaly:
  enabled: true
  error_threshold: 10        # 10 5xx errors
  window_seconds: 60         # 1-minute window
  status_codes:
    - 500
    - 502
    - 503
    - 504

geo_blocking:
  enabled: false             # Planned feature
  blocked_countries:
    - CN
    - RU
    - KP
```

### Application Settings (`config/local.yaml`)

```yaml
database:
  url: "sqlite:///seclog.db"
  echo: false               # SQL query logging
  
api:
  host: "0.0.0.0"
  port: 8000
  workers: 1
  reload: true              # Development only

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/gwc-siem.log"

retention:
  events_days: 30           # Keep events for 30 days
  alerts_days: 90           # Keep alerts for 90 days
```

---

## 🔍 Usage Examples

### Processing Different Log Types

```bash
# SSH authentication logs
tail -f /var/log/auth.log | python cli/app.py --stdin --kind auth

# Nginx access logs
python cli/app.py --file /var/log/nginx/access.log --kind nginx

# Custom log format
python cli/app.py --file custom.log --kind custom --parser custom_parser.py
```

### API Integration

```python
import requests

# Upload log file
with open('auth.log', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/ingest',
        files={'file': f},
        data={'log_type': 'auth'}
    )

# Get alerts
alerts = requests.get('http://localhost:8000/alerts?limit=10').json()
for alert in alerts:
    print(f"Alert: {alert['rule_name']} - {alert['description']}")
```

### Dashboard Monitoring

The web dashboard provides:
- **Real-time Alert Feed**: Live updates of new security alerts
- **Event Timeline**: Chronological view of all processed events
- **Statistics Panel**: System metrics and detection rule performance
- **Log Upload Interface**: Drag-and-drop file upload with progress tracking

---

## 🐛 Troubleshooting

### Common Issues

#### Database Errors
```bash
# Reset database
rm seclog.db
python -c "from storage.database import init_db; init_db()"
```

#### Permission Errors
```bash
# Fix log file permissions
chmod 644 /var/log/auth.log
chmod 755 /var/log/nginx/
```

#### API Not Starting
```bash
# Check port availability
netstat -an | grep :8000

# Check Python dependencies
pip check

# Verify configuration
python -c "import yaml; yaml.safe_load(open('config/local.yaml'))"
```

### Debug Mode

```bash
# Enable debug logging
export GWCSIEM_LOG_LEVEL=DEBUG

# Run with verbose output
uvicorn api.main:app --reload --log-level debug

# Check database contents
sqlite3 seclog.db ".tables"
sqlite3 seclog.db "SELECT * FROM alerts LIMIT 5;"
```

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

## 📌 Roadmap & Future Features

### 🎯 Current Sprint (v1.1)
- [ ] **Apache Access Log Parser**: Support for Apache Common Log Format
- [ ] **Real-time Log Monitoring**: File watcher for continuous log processing
- [ ] **Alert Notifications**: Email and webhook integrations
- [ ] **Performance Optimizations**: Batch processing and caching improvements

### 🚀 Next Release (v1.2)
- [ ] **Advanced Detection Rules**: ML-based anomaly detection
- [ ] **GeoIP Integration**: Location-based threat analysis
- [ ] **Custom Dashboard Widgets**: Configurable monitoring panels
- [ ] **Multi-tenant Support**: Isolated environments for different users

### 🔮 Future Vision (v2.0+)
- [ ] **Distributed Architecture**: Multi-node deployment support
- [ ] **Threat Intelligence Integration**: IOC feeds and reputation services
- [ ] **Compliance Reporting**: PCI DSS, SOX, HIPAA report generators
- [ ] **Machine Learning Pipeline**: Behavioral analysis and predictive alerts
- [ ] **Container Security**: Kubernetes security event monitoring
- [ ] **SIEM Connectors**: Integration with Splunk, ELK, QRadar

### 🤝 Community Requested Features
- [ ] **Mobile Dashboard**: Responsive design for mobile monitoring
- [ ] **Plugin System**: Third-party extension support
- [ ] **Cloud Deployment**: AWS/Azure/GCP deployment templates
- [ ] **MITRE ATT&CK Mapping**: Technique classification for alerts

*Want to contribute to any of these features? Check out our [CONTRIBUTING.md](CONTRIBUTING.md) guide!*

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
