<div align="center">
  <img width="1536" height="1024" alt="GWC SIEM Dashboard" src="https://github.com/user-attachments/assets/17e7065e-791d-473f-9066-cdbde083e32e" />

# GWC-SIEM 🛡️

  <p>A powerful mini-SIEM solution for home labs and Hacktoberfest contributions</p>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Discord](https://img.shields.io/discord/YOUR_DISCORD_ID?label=Join%20Discord&logo=discord)](https://discord.gg/YMJp48qbwR)

</div>

## 📖 Overview

GWC-SIEM is a lightweight Security Information and Event Management system designed for home labs and learning environments. It processes common log formats, detects security events, and provides multiple interfaces for monitoring and analysis.

## ✨ Key Features

- 🔍 **Advanced Log Processing**

  - Support for `auth.log` and Nginx access logs
  - Extensible parser architecture
  - Real-time log ingestion

- 🚨 **Intelligent Detection**

  - SSH brute-force attempt detection
  - HTTP 5xx error burst monitoring
  - Configurable detection thresholds via YAML

- 💾 **Efficient Storage**

  - SQLite backend for portability
  - Optimized query performance
  - Built-in data retention policies

- 🖥️ **Multiple Interfaces**
  - Modern FastAPI REST API
  - Interactive Web Dashboard
  - Command-line Interface (CLI)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/<your-username>/gwc-siem.git

# Navigate to project directory
cd gwc-siem

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -e .
```

### Running the Application

1. **Start the API Server**

```bash
uvicorn api.main:app --reload --port 8000
```

2. **Access the Dashboard**

- Open [http://localhost:8000](http://localhost:8000) in your browser
- Upload sample logs from `sample_data/` directory

3. **Use the CLI**

```bash
python cli/app.py --file sample_data/auth.log --kind auth
```

## 🏗️ Architecture

```
gwc-siem/
├── api/            # FastAPI application
├── core/           # Core SIEM functionality
│   ├── parsers/    # Log parsers
│   └── detections/ # Detection rules
├── storage/        # Database operations
├── web/           # Frontend dashboard
└── cli/           # Command-line interface
```

## 🧪 Development

### Setting Up Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"
```
