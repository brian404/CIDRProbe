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
                port_text = colored(port, "green")
            else:
                status_text = colored(f"{status}", "magenta")  # Use magenta as a fallback color
                port_text = colored(port, "red")
        except requests.exceptions.RequestException:
            status_text = colored("Failed to connect", "red")
            port_text = colored(port, "red")
        print(f"{str(ip):<15}{port_text:<7}{status_text}")

def main():
    print("CIDR Probe - Scan CIDR Range\n")
    while True:
        cidr = input("Enter the CIDR range (e.g., 192.168.0.0/24): ")
        try:
            ip_network = ipaddress.ip_network(cidr)
            break
        except ValueError:
            print("Invalid CIDR range. Please try again.\n")
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
