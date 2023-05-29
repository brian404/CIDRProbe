import ipaddress
import requests
from termcolor import colored

def scan_cidr(cidr, port):
    ip_network = ipaddress.ip_network(cidr)
    
    print(f"\nScanning CIDR range: {cidr}")
    print(f"Port: {port}\n")
    print("IP\t\tPort\tStatus")
    print("--------------------------------------")

    for ip in ip_network.hosts():
        try:
            url = f"http://{ip}:{port}"
            response = requests.get(url, timeout=1)
            status = "Open" if response.status_code == 200 else "Closed"
            status_text = colored(status, "green" if status == "Open" else "red")
            print(f"{ip}\t{port}\t{status_text}")
        except requests.exceptions.RequestException:
            print(f"{ip}\t{port}\tFailed to connect")
        except KeyboardInterrupt:
            print("\nScan interrupted by user.")
            break

def main():
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan (default is 80): ") or "80"
    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
