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

**RECONION** is an ethical **OSINT reconnaissance framework** that routes traffic  
through the **Tor network** to safely collect **publicly available intelligence** from:

- `.onion` services (dark web)
- Normal clearnet websites
- REST / API endpoints

It performs **passive, read-only analysis** focused on **intelligence gathering**,  
**risk assessment**, and **analyst-ready reporting** — **not exploitation**.

---

## ✨ Features

### 🧅 Tor & OSINT Core
- Automatic Tor proxy detection (9050 / 9150)
- Onion service availability checks
- Clearnet website analysis
- API endpoint identification
- Read-only & OSINT-safe requests

### 🧠 Intelligence & Analysis
- Content & keyword analysis (categorized)
- Intent classification (Scam / Crypto / Malware / Informational)
- Passive security misconfiguration checks
- Technology & stack fingerprinting (headers + HTML meta)
- Human-readable AI-style site summary (rule-based)

### 🚨 Risk Assessment
- Scam Score generation (**0–100**)
- Risk level identification (Low / Medium / High)
- Heuristic scoring (no external APIs)

### 📊 Reporting
- TXT report (default)
- JSON output (`--json`)
- CSV output (`--csv`)
- **HTML Dashboard UI (`--html`)**
  - Offline SOC-style dashboard
  - Risk score bars
  - Intent & summary cards
  - Analyst-friendly view

### 🧠 Analysis Details

🔐 Passive Security Checks

Missing security headers (CSP, X-Frame-Options, etc.)

Header-based misconfiguration indicators

No intrusive testing

### 🧩 Technology Fingerprinting

Server header identification

HTML meta generator detection

Passive stack inference

---

## ⚠️ Disclaimer

RECONION is intended for **educational and ethical OSINT purposes only**.

- ❌ Do NOT use this tool on systems you do not own or have permission to analyze
- ❌ No exploitation, brute force, or intrusive scanning is performed
- ✅ All analysis is **passive and read-only**

The author is **not responsible for misuse**.

---

## 🛠️ Installation

Clone the repository and install required dependencies:

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
Step 2: Run RECONION (Direct Targets)

Targets are passed directly via CLI (no targets.txt file).
```bash
python reconion.py example.com

```
Multiple Targets
```bash
python reconion.py example.com facebookcorewwwi.onion https://api.github.com
```
Generate JSON Output
```bash
python reconion.py example.com --json
```
Generate CSV Output
```bash
python reconion.py example.com --csv
```
Generate HTML Dashboard
```bash
python reconion.py example.com --html
```
📄 Output Files
| File                              | Description                        |
| --------------------------------- | ---------------------------------- |
| `reconion_results.txt`            | Human-readable intelligence report |
| `reconion_output.json`            | Structured JSON output             |
| `reconion_output.csv`             | CSV output (schema-safe)           |
| `reports/reconion_dashboard.html` | Offline SOC-style dashboard        |

---

##📄 Output Details (reconion_results.txt)

For each target, the report includes:

Target identifier (.onion / domain / API)

Status (Active / Inactive)

HTTP status code

Server header

Content-Type

Page title

Intent classification

Categorized keyword findings

Passive security issues

Detected technology / stack (if available)

Scam score (0–100)

AI-style human-readable summary

Error details (if any)



---

## 🖥️ HTML Dashboard UI

RECONION generates an offline SOC-style dashboard featuring:

Scam score progress bars

Risk color indicators

Intent classification

Technology stack

Security issues

AI-style summaries

Open manually:
```bash
reports/reconion_dashboard.html

```
## 👨‍💻 Developer

Praveen Kumar

Cybersecurity & OSINT Enthusiast

GitHub: https://github.com/Praveenkumar098


## 📜 License

This project is licensed under the MIT License.


## ⭐ Support

If you find RECONION useful:

⭐ Star the repository

🍴 Fork it

🧠 Share it with the OSINT community
