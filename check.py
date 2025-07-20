import sys
import socket
import ssl
import whois
import requests
from urllib.parse import urlparse
import json

def is_url_safe(url):
    result = {
        "url": url,
        "status": "Safe",
        "reasons": []
    }
    try:
        parsed = urlparse(url)
        domain = parsed.hostname

        # WHOIS check
        try:
            w = whois.whois(domain)
            if not w.domain_name:
                result["status"] = "Suspicious"
                result["reasons"].append("Domain has no WHOIS record.")
            else:
                result["reasons"].append("Domain has WHOIS record.")
        except:
            result["status"] = "Suspicious"
            result["reasons"].append("Failed WHOIS lookup.")

        # SSL check
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(3.0)
                s.connect((domain, 443))
                result["reasons"].append("SSL certificate is valid.")
        except:
            result["status"] = "Warning"
            result["reasons"].append("No valid SSL certificate found.")

        # HTTP status check
        try:
            r = requests.get(url, timeout=5)
            if r.status_code >= 400:
                result["status"] = "Warning"
                result["reasons"].append(f"Returned status code: {r.status_code}")
            else:
                result["reasons"].append(f"Returned status code: {r.status_code}")
        except:
            result["status"] = "Dangerous"
            result["reasons"].append("Site not reachable.")

    except Exception as e:
        result["status"] = "Dangerous"
        result["reasons"].append(str(e))

    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 check.py <url>")
        sys.exit(1)
    url = sys.argv[1]
    if not url.startswith("http"):
        url = "http://" + url
    result = is_url_safe(url)
    with open("results/output.json", "w") as f:
        json.dump(result, f, indent=4)
    print(json.dumps(result, indent=4))

