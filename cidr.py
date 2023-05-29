import ipaddress
import requests
from termcolor import colored

def scan_cidr(cidr, port=80):
    ip_network = ipaddress.ip_network(cidr)
    for ip in ip_network.hosts():
        url = f"http://{str(ip)}"
        try:
            response = requests.get(url, timeout=1)
            status = response.status_code
            if status == 200:
                status_text = colored("200 OK", "green")
            else:
                status_text = colored(f"{status}", "magenta")  # Use magenta as a fallback color
        except requests.exceptions.RequestException:
            status_text = colored("Failed to connect", "red")
        print(f"{str(ip):<15}{port:<7}{status_text}")

def main():
    print("CIDR Probe - Scan CIDR Range\n")
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan (default is 80): ")
    if not port:
        port = 80
    print(f"\nScanning CIDR range: {cidr}")
    print(f"Port: {port}\n")
    print("IP             Port   Status      CDN")
    print("--------------------------------------")
    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
