import ipaddress
import nmap
import requests
from termcolor import colored

def scan_cidr(cidr, port):
    nm = nmap.PortScanner()
    ip_network = ipaddress.ip_network(cidr)
    
    print(f"\nScanning CIDR range: {cidr}")
    print(f"Port: {port}\n")
    print("IP\t\tPort\tStatus\t\tHTTP Response")
    print("--------------------------------------")

    for ip in ip_network.hosts():
        try:
            target = str(ip)
            nm.scan(target, arguments=f"-p {port} --open")
            if nm[target].has_tcp(int(port)) and nm[target].tcp(int(port))['state'] == 'open':
                status_text = colored("Open", "green")
                response = requests.get(f"http://{target}:{port}")
                http_status = response.status_code
            else:
                status_text = colored("Closed", "red")
                http_status = ""
            print(f"{ip}\t{port}\t{status_text}\t\t{http_status}")
        except KeyboardInterrupt:
            print("\nScan interrupted by user.")
            break

def main():
    print("  ____ ___ ____  ____  ____            _          ")
    print(" / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ ")
    print("| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \\")
    print("| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/")
    print(" \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|")
    print("\nhttps://t.me/brian_72\n")
    print("CIDR Probe - Scan CIDR Range")
    print("\n")
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan (default is 80): ") or "80"
    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
