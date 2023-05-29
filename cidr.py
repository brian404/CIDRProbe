import socket
import requests
import ipaddress
from termcolor import colored

def scan_cidr(cidr, port):
    try:
        ip_network = ipaddress.ip_network(cidr)
    except ValueError:
        print(colored("Invalid CIDR range. Please enter a valid range.", "red"))
        print(colored("Example: 192.168.0.0/24", "yellow"))
        return

    num_hosts = ip_network.num_addresses

    if num_hosts > 10000:
        confirm = input(colored(f"The provided CIDR range has a large number of hosts ({num_hosts}). "
                                "Scanning such a range may take a long time. "
                                "Do you still want to proceed? (y/n): ", "yellow"))
        if confirm.lower() != 'y':
            print(colored("Scanning operation cancelled.", "yellow"))
            return

    try:
        int_port = int(port)
        if int_port < 1 or int_port > 65535:
            raise ValueError
    except ValueError:
        print(colored("Invalid port number. Please enter a valid port.", "red"))
        print(colored("Example: 80", "yellow"))
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

    print(colored("IP                Port  -Status   HTTP -Status  Location", attrs=["bold"]))
    print("---------------------------------------------------------")

    for ip in ip_network.hosts():
        ip_str = str(ip)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_str, int(port)))
            sock.close()

            if result == 0:
                port_status = colored("Open", "green")
            else:
                port_status = colored("Closed", "red")

            url = f"http://{ip_str}:{port}"
            try:
                response = requests.get(url, allow_redirects=False, timeout=3)
                http_status = response.status_code
                http_response = response.reason
                location = response.headers.get('Location', "")
                print(f"{ip_str:<17} {port:<6} {port_status:<8} {http_status:<10} {http_response:<10} {location}")
            except requests.exceptions.RequestException:
                print(f"{ip_str:<17} {port:<6} {port_status:<8} {colored('N/A', 'blue'):<10} {colored('N/A', 'yellow')}")

        except KeyboardInterrupt:
            print(colored("\nOperation cancelled by user.", "yellow"))
            break

def main():
    print("CIDRProbe - IP Range Scanner")
    print()

    print("Usage Example:")
    print("CIDR Range: 192.168.0.0/24")
    print("Port: 80")
    print()

    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan: ")

    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
