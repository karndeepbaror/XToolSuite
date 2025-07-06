import os
import requests
import socket
import subprocess
from urllib.parse import urljoin
from bs4 import BeautifulSoup

COMMON_PORTS = [21, 22, 80, 443, 3306, 8080]

def banner():
    os.system("clear")
    print("\033[92m")
    print("███╗   ██╗ █████╗ ███████╗ █████╗      ████████╗ ██████╗  ██████╗ ██╗     ")
    print("████╗  ██║██╔══██╗██╔════╝██╔══██╗     ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ")
    print("██╔██╗ ██║███████║███████╗███████║█████╗ ██║   ██║   ██║██║   ██║██║     ")
    print("██║╚██╗██║██╔══██║╚════██║██╔══██║╚════╝ ██║   ██║   ██║██║   ██║██║     ")
    print("██║ ╚████║██║  ██║███████║██║  ██║       ██║   ╚██████╔╝╚██████╔╝███████╗")
    print("╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝       ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝")
    print()
    print("                XToolSuite v1.0 - I SEE YOU 👽")
    print()
    print("  [1] 🔍 Web Scanner     [3] 📡 LAN Mapper       [5] 🧠 OS Fingerprint")
    print("  [2] 🌐 Subdomains      [4] 🔓 Port Scanner     [6] 🛡️ Header Audit")
    print("  [7] 🍪 CORS + Cookies  [8] 🧾 Metadata Xtract  [q] ❌ Exit")
    print()
    print("     🌐 Framework: X Tool Suite | Dev: Karndeep Baror")
    print("     🔗 Telegram: @karnd33p       | 🧠 IG : @karndeepbaror")
    print("\033[0m")

def website_scanner(domain):
    try:
        ip = socket.gethostbyname(domain)
        r = requests.get(f"http://{domain}", timeout=5)
        print(f"IP: {ip}")
        print(f"Server: {r.headers.get('Server', 'Unknown')}")
        print("CMS: WordPress" if "wp-content" in r.text else "CMS: Unknown")
    except Exception as e:
        print("Error:", e)

def subdomain_finder(domain):
    try:
        res = requests.get(f"https://crt.sh/?q=%.{domain}&output=json", timeout=5)
        subs = sorted(set(entry['name_value'] for entry in res.json()))
        for s in subs[:10]:
            print("•", s)
    except:
        print("Subdomain fetch failed")

def lan_ip_mapper():
    ip_base = socket.gethostbyname(socket.gethostname()).rsplit('.', 1)[0]
    print("Scanning your LAN...")
    for i in range(1, 20):
        ip = f"{ip_base}.{i}"
        try:
            socket.gethostbyaddr(ip)
            print(f"✅ Active: {ip}")
        except:
            pass

def port_scanner(domain):
    ip = socket.gethostbyname(domain)
    print(f"Scanning {ip}...")
    for port in COMMON_PORTS:
        try:
            s = socket.socket()
            s.settimeout(0.5)
            if s.connect_ex((ip, port)) == 0:
                print(f"🟢 Port {port} open")
            s.close()
        except:
            continue

def os_fingerprinter(domain):
    ip = socket.gethostbyname(domain)
    try:
        ttl = int(subprocess.check_output(["ping", "-c", "1", ip]).decode().split("ttl=")[1].split()[0])
        print("OS Fingerprint:", "Linux/Unix" if ttl <= 64 else "Windows")
    except:
        print("Ping failed")

def header_auditor(domain):
    try:
        r = requests.get(f"http://{domain}", timeout=5)
        print("Security Headers:")
        for h in r.headers:
            print(f"{h}: {r.headers[h]}")
    except:
        print("Header fetch failed")

def cookie_cors_checker(domain):
    try:
        r = requests.get(f"http://{domain}", timeout=5)
        cors = requests.options(f"http://{domain}", timeout=5)
        print("Cookies:", r.headers.get("Set-Cookie", "None"))
        print("CORS:", cors.headers.get("Access-Control-Allow-Origin", "Not set"))
    except:
        print("CORS or Cookie check failed")

def metadata_extractor(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string if soup.title else "N/A"
        print("Page Title:", title)
        for tag in soup.find_all("meta"):
            print(tag)
    except:
        print("Metadata extraction failed")

def main():
    while True:
        banner()
        choice = input("Choose option (1–8 or q to quit): ").strip()
        if choice == "1":
            website_scanner(input("Domain: "))
        elif choice == "2":
            subdomain_finder(input("Domain: "))
        elif choice == "3":
            lan_ip_mapper()
        elif choice == "4":
            port_scanner(input("Domain: "))
        elif choice == "5":
            os_fingerprinter(input("Domain: "))
        elif choice == "6":
            header_auditor(input("Domain: "))
        elif choice == "7":
            cookie_cors_checker(input("Domain: "))
        elif choice == "8":
            metadata_extractor(input("Full URL (http://...): "))
        elif choice.lower() == "q":
            print("Exiting XToolSuite Tool . Stay ethical [ KK ☠️ ]")
            break
        else:
            print("Invalid choice.")
        input("Press Enter to continue...")

if __name__ == "__main__":
    main()
