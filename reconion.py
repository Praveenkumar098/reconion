import requests
from bs4 import BeautifulSoup
from datetime import datetime
import argparse
import json
import csv
import sys
import os

# =========================
# METADATA
# =========================
VERSION = "1.4"

KEYWORDS = [
    "drugs", "carding", "weapons",
    "malware", "leaks", "crypto",
    "bitcoin", "hacking"
]

HEADERS = {
    "User-Agent": "RECONION-OSINT"
}

# =========================
# BANNER (CORRECT)
# =========================
BANNER = r"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██║██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██║██║   ██║██║╚██╗ ██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝ v1.4
"""

# =========================
# TOR DETECTION
# =========================
def detect_tor():
    for port in [9050, 9150]:
        proxies = {
            "http": f"socks5h://127.0.0.1:{port}",
            "https": f"socks5h://127.0.0.1:{port}"
        }
        try:
            requests.get("https://check.torproject.org", proxies=proxies, timeout=8)
            return proxies, port
        except:
            continue
    return None, None


def normalize(target):
    if target.endswith(".onion") and not target.startswith("http"):
        return "http://" + target
    if not target.startswith("http"):
        return "http://" + target
    return target


# =========================
# ANALYSIS FUNCTIONS
# =========================
def keyword_scan(text):
    return [k for k in KEYWORDS if k in text.lower()]


def calculate_risk(target, keywords, is_api):
    score = 0
    if target.endswith(".onion"):
        score += 2
    if keywords:
        score += 2
    if is_api:
        score += 1

    if score >= 4:
        return "HIGH"
    elif score >= 2:
        return "MEDIUM"
    return "LOW"


def take_screenshot(url, filename):
    try:
        from selenium import webdriver
        from selenium.webdriver.firefox.options import Options

        os.makedirs("screenshots", exist_ok=True)

        options = Options()
        options.add_argument("--headless")

        driver = webdriver.Firefox(options=options)
        driver.get(url)
        driver.save_screenshot(filename)
        driver.quit()

        return "Captured"
    except:
        return "Skipped"


# =========================
# MAIN SCAN
# =========================
def scan_target(target, proxies, screenshot):
    url = normalize(target)
    result = {"Target": target}

    try:
        r = requests.get(url, headers=HEADERS, proxies=proxies, timeout=25)
        ct = r.headers.get("Content-Type", "")

        result["Status"] = "Active"
        result["HTTP_Code"] = r.status_code
        result["Content_Type"] = ct

        if "text/html" in ct:
            soup = BeautifulSoup(r.text, "html.parser")
            text = soup.get_text()
            keywords = keyword_scan(text)
            result["Title"] = soup.title.string if soup.title else "No Title"
            result["Keywords"] = keywords
            is_api = False
        else:
            result["Title"] = "API / Non-HTML"
            result["Keywords"] = []
            is_api = True

        risk = calculate_risk(target, keywords, is_api)
        result["Risk_Score"] = risk

        if screenshot:
            safe = target.replace("://", "_").replace("/", "_")
            filename = f"screenshots/{safe}_{risk}.png"
            result["Screenshot"] = take_screenshot(url, filename)

    except Exception as e:
        result["Status"] = "Inactive"
        result["Error"] = str(e)

    return result


# =========================
# ENTRY POINT
# =========================
def main():
    parser = argparse.ArgumentParser(
        description="RECONION – Tor-based OSINT Reconnaissance Tool"
    )
    parser.add_argument("targets", nargs="+", help="Targets (.onion / website / API)")
    parser.add_argument("--json", action="store_true", help="Save JSON output")
    parser.add_argument("--csv", action="store_true", help="Save CSV output")
    parser.add_argument("--screenshot", action="store_true", help="Capture screenshots")
    parser.add_argument("--version", action="version", version=f"RECONION v{VERSION}")
    args = parser.parse_args()

    print(BANNER)

    proxies, port = detect_tor()
    if not proxies:
        print("[-] Tor not detected. Start Tor Browser.")
        sys.exit(1)

    results = []
    for t in args.targets:
        print(f"[+] Scanning: {t}")
        results.append(scan_target(t, proxies, args.screenshot))

    # TXT output
    with open("reconion_results.txt", "w", encoding="utf-8") as f:
        f.write(f"Generated: {datetime.now()}\nTor Port: {port}\n\n")
        for r in results:
            for k, v in r.items():
                f.write(f"{k}: {v}\n")
            f.write("-" * 60 + "\n")

    if args.json:
        with open("reconion_output.json", "w", encoding="utf-8") as jf:
            json.dump(results, jf, indent=4)

    if args.csv:
        with open("reconion_output.csv", "w", newline="", encoding="utf-8") as cf:
            writer = csv.DictWriter(cf, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)

    print("\n✅ RECONION completed successfully")


if __name__ == "__main__":
    main()
