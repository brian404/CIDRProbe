import sys
import requests
from termcolor import colored
from tabulate import tabulate

BANNER = '''
  ____ ___ ____  ____  ____            _    
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \\
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/

CIDR Probe - Scan CIDR Range

'''

CDN_PROVIDERS = {
    "CloudFront": "cloudfront.net",
    "Cloudflare": "cloudflare",
    # Add more CDN providers here
}

def detect_cdn(url):
    for provider, domain in CDN_PROVIDERS.items():
        if domain in url:
            return provider
    return ""

def main():
    print(BANNER)
    
    if len(sys.argv) > 1 and sys.argv[1] == "-p":
        print("Usage: python cidr.py [<CIDR>]")
        print("Example: python cidr.py 10.0.0.0/24")
        return
    
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan (default is 80): ")
    port = int(port) if port else 80
    
    print(f"\nScanning CIDR range: {cidr}")
    print(f"Port: {port}\n")
    
    headers = ["IP", "Port", "Status", "CDN"]
    rows = []
    
    try:
        ips = cidr.split('/')[0]
        prefix = int(cidr.split('/')[1])
        start_ip = sum([int(x) << y for x, y in zip(ips.split('.'), [24, 16, 8, 0])])
        end_ip = start_ip + 2 ** (32 - prefix)
        
        for ip in range(start_ip, end_ip):
            ip_address = '.'.join([str(ip >> (y << 3) & 0xFF) for y in [3, 2, 1, 0]])
            url = f"http://{ip_address}:{port}"
            
            try:
                response = requests.get(url, timeout=1)
                
                if response.status_code == 200:
                    status = colored("Open", "green")
                else:
                    status = colored("Closed", "magenta")
                
                cdn = detect_cdn(response.url)
                rows.append([ip_address, port, status, cdn])
            except requests.exceptions.RequestException:
                rows.append([ip_address, port, colored("Failed to connect", "red"), ""])
    
    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")
    
    print(tabulate(rows, headers=headers))


if __name__ == "__main__":
    main()
