# RECONION

Build Status • MIT License • Tor Compatible • Python 3

A simple and powerful **Tor-based OSINT reconnaissance tool**  
written in **pure Python** for inspecting:

🧅 Deep Web / Onion services  
🌐 Clearnet websites  
🔌 API endpoints  

Compatible with **Python 3.x** 🎉

---

## 🔍 About RECONION

**RECONION** is an ethical OSINT reconnaissance tool that routes traffic  
through the **Tor network** to safely collect **public intelligence** from:

- `.onion` services (dark web)
- Normal websites
- REST API endpoints

It focuses on **metadata extraction**, not exploitation.

---

## ✨ Features

- 🧅 Onion service availability checks
- 🌐 Website reconnaissance
- 🔌 API endpoint detection
- 🧠 Title, headers & content-type analysis
- 🕵️ Subdomain enumeration (clearnet only)
- 🔄 Automatic Tor port detection (9050 / 9150)
- 📄 Clean recon report generation
- ⚠️ Read-only & OSINT-safe

---

## ⚠️ Disclaimer

RECONION is intended for **educational and ethical OSINT purposes only**.  
Do **NOT** use this tool on systems you do not own or have permission to analyze.  
The author is **not responsible** for misuse.

---

## 🛠️ Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/Praveenkumar098/reconion.git
cd reconion
pip install -r requirements.txt

```
▶️ Running the Tool
Step 1: Start Tor

Windows

Open Tor Browser

Wait until it shows Connected

Linux
```bash
sudo service tor start

```
Step 2: Add Targets

Edit the targets.txt file and add one target per line:
```Text
duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion
example.com
https://api.github.com

```
Step 3: Run RECONION
```bash
python reconion.py

```
📄 Output
reconion_results.txt

Target status (Active / Inactive)

HTTP status code

Server header

Content-Type

Page title

Error details (if any)

subdomains.txt

Enumerated subdomains

Generated only for clearnet domains

---
👨‍💻 Developer

Praveen Kumar

Cybersecurity & OSINT Enthusiast

GitHub: https://github.com/Praveenkumar098


