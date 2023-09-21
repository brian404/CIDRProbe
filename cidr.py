import ipaddress
import ping3
from termcolor import colored
import socket
import requests

def scan_cidr(cidr):
    try:
        ip_network = ipaddress.ip_network(cidr)
    except ValueError:
        print(colored("Invalid CIDR range. Please enter a valid range.", "red"))
        print(colored("Example: 192.168.0.0/24", "yellow"))
        return

    print(colored(r'''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  ''', "white"))
    print(colored("Contact me via Telegram for any issues.", "white"))
    print(colored("https://t.me/brian_72", "white"))
    print()

    print(colored("IP                Status      Hostname       HTTP Status", attrs=["bold"]))
    print("------------------------------------------------------------")

    for ip in ip_network.hosts():
        ip_str = str(ip)
        try:
            response_time = ping3.ping(ip_str)
            if response_time is not None:
                status = colored("Alive", "green")
            else:
                status = colored("Not Responding", "red")

            try:
                hostname, _, _ = socket.gethostbyaddr(ip_str)
            except socket.herror:
                hostname = colored("N/A", "yellow")

            try:
                response = requests.get(f"http://{ip_str}", timeout=5)
                http_status = f"{response.status_code} {response.reason}"
            except (requests.RequestException, ValueError):
                http_status = colored("N/A", "yellow")

            print(f"{ip_str:<17} {status:<10} {hostname:<15} {http_status}")

        except KeyboardInterrupt:
            print(colored("\nOperation cancelled by user.", "yellow"))
            break

def main():
    print("CIDRProbe - IP Range Scanner")
    print()

    print("Usage Example:")
    print("CIDR Range: 192.168.0.0/24")
    print()

    cidr = input("Enter the CIDR range: ")

    scan_cidr(cidr)

if __name__ == "__main__":
    main()
