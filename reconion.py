import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime
import argparse
import sys

# =========================
# RECONION METADATA
# =========================
VERSION = "1.0"

BANNER = r"""
██████╗ ███████╗ ██████╗ ██████╗ ███╗   ██╗██╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔═══██╗████╗  ██║██║██╔═══██╗████╗  ██║
██████╔╝█████╗  ██║     ██║   ██║██╔██╗ ██║██║██║   ██║██╔██╗ ██║
██╔══██╗██╔══╝  ██║     ██║   ██║██║╚██╗██║██║██║   ██║██║╚██╗██║
██║  ██║███████╗╚██████╗╚██████╔╝██║ ╚████║██║╚██████╔╝██║ ╚████║
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝ v1.0
"""

HEADERS = {
    "User-Agent": "RECONION-OSINT"
}

# =========================
# TOR AUTO-DETECTION
# =========================
def detect_tor_proxy():
    for port in [9050, 9150]:
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
            continue
    return None, None


# =========================
# CORE FUNCTIONS
# =========================
def normalize_url(target):
    if target.endswith(".onion") and not target.startswith("http"):
        return "http://" + target
    if not target.startswith("http"):
        return "http://" + target
    return target


def scan_target(target, proxies, tor_enabled):
    url = normalize_url(target)
    result = {}

    try:
        r = requests.get(
            url,
            headers=HEADERS,
            proxies=proxies if tor_enabled else None,
            timeout=25
        )

        result["Status"] = "Active"
        result["HTTP_Code"] = r.status_code
        result["Server"] = r.headers.get("Server", "Unknown")
        result["Content-Type"] = r.headers.get("Content-Type", "Unknown")

        if "text/html" in r.headers.get("Content-Type", ""):
            soup = BeautifulSoup(r.text, "html.parser")
            result["Title"] = soup.title.string.strip() if soup.title else "No Title"
        else:
            result["Title"] = "Non-HTML / API Endpoint"

    except Exception as e:
        result["Status"] = "Inactive"
        result["Error"] = str(e)

    return result


def find_subdomains(domain, proxies, tor_enabled):
    subdomains = set()
    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    try:
        r = requests.get(
            url,
            proxies=proxies if tor_enabled else None,
            timeout=30
        )
        if r.status_code == 200:
            for entry in r.json():
                names = entry.get("name_value", "")
                for name in names.split("\n"):
                    if "*" not in name:
                        subdomains.add(name.strip())
    except:
        pass

    return subdomains


# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser(
        description="RECONION - Tor-based OSINT Reconnaissance Tool"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"RECONION v{VERSION}"
    )

    parser.add_argument(
        "-t", "--target",
        help="Single target (onion / website / API)"
    )

    parser.add_argument(
        "-f", "--file",
        help="Targets file (default: targets.txt)"
    )

    parser.add_argument(
        "-o", "--output",
        default="reconion_results.txt",
        help="Output file name"
    )

    parser.add_argument(
        "--active",
        action="store_true",
        help="Save only active targets to output"
    )

    args = parser.parse_args()

    print(BANNER)

    proxies, tor_port = detect_tor_proxy()
    tor_enabled = True if proxies else False

    print(f"[+] Tor Used : {tor_enabled}")
    print(f"[+] Tor Port : {tor_port if tor_enabled else 'N/A'}\n")

    targets = []

    if args.target:
        targets.append(args.target)

    elif args.file:
        try:
            with open(args.file, "r") as f:
                targets = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("[-] Target file not found")
            sys.exit(1)

    else:
        try:
            with open("targets.txt", "r") as f:
                targets = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("[-] targets.txt not found")
            sys.exit(1)

    with open(args.output, "w", encoding="utf-8") as report, \
         open("subdomains.txt", "w", encoding="utf-8") as subs:

        report.write("RECONION RECON REPORT\n")
        report.write(f"Generated : {datetime.now()}\n")
        report.write(f"Tor Used  : {tor_enabled}\n")
        report.write(f"Tor Port  : {tor_port if tor_enabled else 'N/A'}\n\n")

        for target in targets:
            print(f"[+] Scanning: {target}")
            data = scan_target(target, proxies, tor_enabled)

            if args.active and data["Status"] != "Active":
                continue

            report.write(f"Target: {target}\n")
            for k, v in data.items():
                report.write(f"{k}: {v}\n")
            report.write("-" * 60 + "\n")

            if not target.endswith(".onion"):
                domain = urlparse(normalize_url(target)).netloc
                subs_found = find_subdomains(domain, proxies, tor_enabled)
                for s in sorted(subs_found):
                    subs.write(s + "\n")

    print("\n✅ RECONION completed")
    print(f"📄 Output : {args.output}")
    print("📄 Subdomains : subdomains.txt")


if __name__ == "__main__":
    main()

