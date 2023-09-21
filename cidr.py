import ipaddress
import ping3
from termcolor import colored
import socket
import subprocess

def get_http_status(ip_str):
    try:
        cmd = ["curl", "-i", ip_str]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout
        if "HTTP/1.1" in output:
            status_line = output.splitlines()[0]
            status_code = status_line.split()[1]
            return status_code
        else:
            return colored("N/A", "yellow")
    except subprocess.TimeoutExpired:
        return colored("Timeout", "red")
    except Exception:
        return colored("N/A", "yellow")

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

            http_status = get_http_status(ip_str)

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
