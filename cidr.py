import ipaddress
import requests
import argparse
import socket
import time

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

def scan_cidr(cidr, ports, timeout):
    try:
        network = ipaddress.ip_network(cidr)
    except ValueError:
        print("Invalid CIDR range entered. Please try again.")
        return

    alive_ips = []

    banner = '''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \\
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
'''

    print(banner)

    print("Scanning...")
    time.sleep(1)

    for ip in network.hosts():
        ip_str = str(ip)
        print(f"{ip_str} - ", end='')

        for port in ports:
            try:
                response = requests.get(f"http://{ip_str}:{port}", timeout=timeout)
                if response.status_code == requests.codes.ok:
                    alive_ips.append(ip_str)
                    print(f"{port}: {response.status_code} {response.reason}")
                else:
                    print(f"{port}: {response.status_code} {response.reason}")
            except requests.exceptions.RequestException:
                print(f"{port}: Connection error")

        time.sleep(0.5)

    if alive_ips:
        with open("alive.txt", "w") as file:
            file.write("\n".join(alive_ips))
        print("Alive IP addresses saved to alive.txt")
    else:
        print("No alive IP addresses found within the specified CIDR range.")

    print("\nFor more information and updates, visit:")
    print("GitHub: [CIDRProbe](https://github.com/brian404/CIDRProbe)")

def main():
    parser = argparse.ArgumentParser(description="Advanced CIDR Scanner")
    parser.add_argument("cidr", type=str, help="CIDR range to scan")
    parser.add_argument("-p", "--port", nargs="+", default=[], help="Ports to check (optional)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout for HTTP requests (default: 1 second)")
    args = parser.parse_args()

    if args.port and "All" in args.port:
        ports = [80, 443]
    else:
        ports = args.port

    scan_cidr(args.cidr, ports, args.timeout)

if __name__ == "__main__":
    main()
