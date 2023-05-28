import ipaddress
import requests
import argparse
import socket
from termcolor import colored
import time

BANNER = r"""
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
"""

def is_port_open(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                return True
            else:
                return False
    except socket.error:
        return False

def scan_cidr(cidr, port, timeout):
    try:
        network = ipaddress.ip_network(cidr)
    except ValueError:
        print("Invalid CIDR range entered. Please try again.")
        return

    alive_ips = []

    print(BANNER)
    print(f"\nScanning CIDR range: {cidr}\n")

    for ip in network.hosts():
        ip_str = str(ip)

        try:
            response = requests.get(f"http://{ip_str}", timeout=timeout)
            if response.status_code == requests.codes.ok:
                if port and is_port_open(ip_str, port):
                    alive_ips.append(ip_str)
                    print(colored(f"Alive IP: {ip_str}, Response: {response.status_code}", "green"))
                else:
                    print(colored(f"Non-alive IP: {ip_str}, Response: {response.status_code}", "red"))
            else:
                if port and is_port_open(ip_str, port):
                    print(colored(f"Alive IP (HTTP error): {ip_str}, Response: {response.status_code}", "green"))
                else:
                    print(colored(f"Non-alive IP (HTTP error): {ip_str}, Response: {response.status_code}", "red"))
        except requests.exceptions.RequestException:
            if port and is_port_open(ip_str, port):
                print(colored(f"Alive IP (Connection error): {ip_str}", "green"))
            else:
                print(colored(f"Non-alive IP (Connection error): {ip_str}", "red"))

        time.sleep(0.1)  # Delay for better visualization

    if alive_ips:
        with open("alive.txt", "w") as file:
            file.write("\n".join(alive_ips))
        print("\nAlive IP addresses saved to alive.txt")
    else:
        print("\nNo alive IP addresses found within the specified CIDR range.")

def main():
    parser = argparse.ArgumentParser(description="Advanced CIDR Scanner")
    parser.add_argument("cidr", type=str, help="CIDR range to scan")
    parser.add_argument("-p", "--port", type=str, help="Port(s) to check")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout for HTTP requests (default: 1 second)")
    args = parser.parse_args()

    scan_cidr(args.cidr, args.port, args.timeout)

if __name__ == "__main__":
    main()
