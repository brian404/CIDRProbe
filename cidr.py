import socket
import requests
import ipaddress
from termcolor import colored

def scan_cidr(cidr, dns_lookup_enabled=False):
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

    print(colored("IP                Port  -Status", attrs=["bold"]))
    print("--------------------------------")

    for ip in ip_network.hosts():
        ip_str = str(ip)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_str, 80))
            sock.close()

            if result == 0:
                port_status = colored("Open", "green")
            else:
                port_status = colored("Closed", "red")

            print(f"{ip_str:<17} {port_status:<8}")

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
    dns_lookup_enabled = input("Perform DNS lookup for each IP? (y/n): ").lower() == "y"

    scan_cidr(cidr, dns_lookup_enabled)

if __name__ == "__main__":
    main()
