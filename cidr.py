import ipaddress
import requests
import signal
import sys
from colorama import Fore, Style

# Banner
banner = '''
  ____ ___ ____  ____  ____            _    
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \\
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ 
'''

# Your GitHub link
github_link = 'https://github.com/brian404/'

def scan_cidr(cidr, port):
    try:
        network = ipaddress.ip_network(cidr)
        print(f"\nScanning CIDR range: {cidr} on port {port}\n")

        # Handle Ctrl+C to cancel the operation
        def signal_handler(signal, frame):
            print("\nOperation cancelled by user.")
            sys.exit(0)

        signal.signal(signal.SIGINT, signal_handler)

        for ip in network.hosts():
            url = f"http://{ip}:{port}"
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    print(f"[+] {ip} - Port {port}: {Fore.GREEN}Open{Style.RESET_ALL}")
                else:
                    print(f"[-] {ip} - Port {port}: {Fore.MAGENTA}Closed{Style.RESET_ALL}")
            except requests.exceptions.RequestException as e:
                print(f"[-] {ip} - Failed to connect: {e}")

    except ValueError as e:
        print("Invalid CIDR range. Please provide a valid range.")

def main():
    print(banner)
    print(f"GitHub: {github_link}\n")

    cidr = input("Enter the CIDR range to scan (e.g., 192.168.0.0/24): ")
    port = input("Enter the port number to scan (default is 80): ")

    if not port:
        port = 80

    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
