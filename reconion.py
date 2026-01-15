import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import json
import csv
import sys
import os
from collections import Counter

# =========================
# METADATA
# =========================
VERSION = "2.1"
HEADERS = {"User-Agent": "RECONION-OSINT"}

# =========================
# TERMINAL LOGO
# =========================
BANNER = r"""
 ██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗ ██████╗ ███╗   ██╗
 ██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██║██╔═══██╗████╗  ██║
 ██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
 ██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██║██║   ██║██║╚██╗██║
 ██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║╚██████╔╝██║ ╚████║
 ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝
              Tor-based OSINT Reconnaissance Framework
                           v2.1
"""

# =========================
# KEYWORD CATEGORIES
# =========================
KEYWORD_CATEGORIES = {
    "Scam": ["scam", "fraud", "fake", "phishing"],
    "Crypto": ["crypto", "bitcoin", "wallet", "investment"],
    "Malware": ["malware", "hacking", "exploit", "ransomware"],
    "Drugs": ["drugs", "cocaine", "heroin", "lsd"],
    "Weapons": ["weapons", "guns", "ammo"]
}

# =========================
# TOR DETECTION
# =========================
def detect_tor():
    for port in (9050, 9150):
        proxies = {
            "http": f"socks5h://127.0.0.1:{port}",
            "https": f"socks5h://127.0.0.1:{port}"
        }
        try:
            requests.get(
                "https://check.torproject.org",
                proxies=proxies,
                timeout=8
            )
            return proxies, port
        except:
            pass
    return None, None


def normalize(target):
    if target.endswith(".onion") and not target.startswith("http"):
        return "http://" + target
    if not target.startswith("http"):
        return "http://" + target
    return target


# =========================
# PASSIVE SECURITY CHECKS
# =========================
def security_checks(headers):
    issues = []
    if "X-Frame-Options" not in headers:
        issues.append("Missing X-Frame-Options")
    if "Content-Security-Policy" not in headers:
        issues.append("Missing Content-Security-Policy")
    if "X-Content-Type-Options" not in headers:
        issues.append("Missing X-Content-Type-Options")
    return issues


def tech_fingerprint(headers, soup):
    tech = []
    if headers.get("Server"):
        tech.append(headers.get("Server"))
    gen = soup.find("meta", attrs={"name": "generator"})
    if gen and gen.get("content"):
        tech.append(gen.get("content"))
    return tech


# =========================
# CONTENT ANALYSIS
# =========================
def analyze_content(text):
    findings = Counter()
    for category, words in KEYWORD_CATEGORIES.items():
        for w in words:
            if w in text:
                findings[category] += 1
    return findings


def classify_intent(findings):
    if not findings:
        return "Informational / Unknown"
    return max(findings, key=findings.get)


def calculate_scam_score(findings, is_onion, security_issues):
    score = 0
    if "Scam" in findings:
        score += 40
    if "Crypto" in findings:
        score += 20
    if "Malware" in findings:
        score += 20
    if is_onion:
        score += 10
    score += min(len(security_issues) * 5, 20)
    return min(score, 100)


def ai_summary(target, intent, score, tech):
    summary = f"The site {target} appears to be related to {intent.lower()} activity. "
    if score >= 70:
        summary += "It shows strong indicators of high-risk or scam-related behavior. "
    elif score >= 40:
        summary += "It shows moderate risk indicators based on passive analysis. "
    else:
        summary += "It appears low risk based on the available indicators. "

    if tech:
        summary += "Observed technologies include: " + ", ".join(tech) + "."

    return summary


# =========================
# SCAN TARGET
# =========================
def scan_target(target, proxies):
    url = normalize(target)
    result = {"Target": target}

    try:
        r = requests.get(url, headers=HEADERS, proxies=proxies, timeout=25)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text().lower()

        server_header = r.headers.get("Server", "N/A")
        content_type = r.headers.get("Content-Type", "N/A")
        page_title = soup.title.string.strip() if soup.title and soup.title.string else "N/A"

        sec_issues = security_checks(r.headers)
        tech = tech_fingerprint(r.headers, soup)
        findings = analyze_content(text)
        intent = classify_intent(findings)
        score = calculate_scam_score(findings, target.endswith(".onion"), sec_issues)
        summary = ai_summary(target, intent, score, tech)

        result.update({
            "Status": "Active",
            "HTTP_Code": r.status_code,
            "Server_Header": server_header,
            "Content_Type": content_type,
            "Page_Title": page_title,
            "Intent": intent,
            "Keyword_Findings": dict(findings),
            "Security_Issues": sec_issues,
            "Technology": tech,
            "Scam_Score": score,
            "AI_Summary": summary
        })

    except Exception as e:
        result["Status"] = "Inactive"
        result["Error"] = str(e)

    return result


# =========================
# HTML DASHBOARD
# =========================
def generate_html(results):
    os.makedirs("reports", exist_ok=True)
    path = "reports/reconion_dashboard.html"

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"""
<!DOCTYPE html>
<html>
<head>
<title>RECONION Dashboard</title>
<style>
body {{ background:#0d1117; color:#e6edf3; font-family: Arial; }}
.card {{ background:#161b22; margin:20px; padding:20px; border-radius:12px; }}
.low {{ color:#2ea043; }}
.medium {{ color:#d29922; }}
.high {{ color:#f85149; }}
.bar {{ height:12px; background:#30363d; border-radius:6px; }}
.fill {{ height:100%; }}
</style>
</head>
<body>

<h1 align="center">🧅 RECONION Intelligence Dashboard</h1>
<p align="center">Generated: {datetime.now()}</p>
""")

        for r in results:
            score = r.get("Scam_Score", 0)
            if score >= 70:
                cls, col = "high", "#f85149"
            elif score >= 40:
                cls, col = "medium", "#d29922"
            else:
                cls, col = "low", "#2ea043"

            f.write(f"""
<div class="card">
<h2>{r.get("Target")}</h2>
<b>Status:</b> {r.get("Status")}<br>
<b>HTTP Code:</b> {r.get("HTTP_Code", "N/A")}<br>
<b>Server:</b> {r.get("Server_Header")}<br>
<b>Content-Type:</b> {r.get("Content_Type")}<br>
<b>Page Title:</b> {r.get("Page_Title")}<br><br>

<b>Intent:</b> {r.get("Intent")}<br>
<b>Scam Score:</b> <span class="{cls}">{score}/100</span>
<div class="bar"><div class="fill" style="width:{score}%; background:{col};"></div></div>

<b>Technology:</b> {", ".join(r.get("Technology", []))}<br>
<b>Security Issues:</b> {", ".join(r.get("Security_Issues", []))}<br>
<b>AI Summary:</b><br>{r.get("AI_Summary")}
</div>
""")

        f.write("</body></html>")

    return path


# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser(description="RECONION v2.1 – Advanced OSINT Tool")
    parser.add_argument("targets", nargs="+", help="Targets (.onion / clearnet)")
    parser.add_argument("--json", action="store_true", help="Save JSON output")
    parser.add_argument("--csv", action="store_true", help="Save CSV output")
    parser.add_argument("--html", action="store_true", help="Generate HTML dashboard")
    args = parser.parse_args()

    print(BANNER)

    proxies, port = detect_tor()
    if not proxies:
        print("[-] Tor not detected. Start Tor Browser.")
        sys.exit(1)

    results = [scan_target(t, proxies) for t in args.targets]

    # TXT OUTPUT
    with open("reconion_results.txt", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, indent=2) + "\n\n")

    # JSON OUTPUT
    if args.json:
        with open("reconion_output.json", "w", encoding="utf-8") as jf:
            json.dump(results, jf, indent=4)

    # CSV OUTPUT
    if args.csv:
        fields = sorted({k for r in results for k in r})
        with open("reconion_output.csv", "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=fields)
            writer.writeheader()
            writer.writerows(results)

    # HTML DASHBOARD
    if args.html:
        report = generate_html(results)
        print(f"[+] HTML dashboard generated: {report}")

    print("\n✅ RECONION completed successfully")


if __name__ == "__main__":
    main()

