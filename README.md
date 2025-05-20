# UniFi to Pi-hole DNS Sync

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/Platform-macOS%20%7C%20Linux-lightgrey.svg)]()

This Python script connects to a UniFi Express gateway to extract current DHCP leases and syncs them into your Pi-hole’s local DNS configuration (`custom.list`). It ensures your network devices are addressable by hostname and updates Pi-hole only when changes are detected.

---

## 🔧 Features

- 🔐 SSH key-based authentication (no passwords needed)
- 📡 Parses IP & hostname leases from UniFi Express
- 🧠 Avoids duplicate or unnecessary Pi-hole writes
- 💾 Automatically backs up `custom.list` before changes
- ♻️ Restarts Pi-hole DNS resolver only when needed

---

## 📦 Requirements

- Python 3.7+
- Pi-hole installed and reachable via SSH
- UniFi Express running and SSH-enabled
- SSH keys set up for both devices

---

## 🚀 Setup

### 1. Clone this repo:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

2. Create and activate a virtual environment:
```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create your .env file:
```bash
cp .env.example .env
```

Edit .env and fill in your actual connection details.

---

## 📄 Example .env File

```
UNIFI_HOST=192.168.1.1
UNIFI_USER=your_unifi_user
PIHOLE_HOST=192.168.1.145
PIHOLE_USER=your_pihole_user
SSH_KEY_PATH=/path/to/your/ssh_key
```

---

## ▶️ How to Run

```bash
python sync_dns_to_pihole.py
```

## 📄 License

This project is licensed under the [MIT License](LICENSE).