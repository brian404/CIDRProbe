import ipaddress
import requests
import argparse
import socket

# Banner
banner = r'''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  
CIDRProbe - Advanced CIDR Scanner
'''

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

    print(f"Scanning CIDR range: {cidr}")

    for ip in network.hosts():
        ip_str = str(ip)

        try:
            for port in ports:
                response = requests.get(f"http://{ip_str}:{port}", timeout=timeout)
                if response.status_code == requests.codes.ok:
                    alive_ips.append(ip_str)
                    print(f"Alive IP: {ip_str}, Port: {port}, Response: {response.status_code}")
        except requests.exceptions.RequestException:
            pass

    if alive_ips:
        with open("alive.txt", "w") as file:
            file.write("\n".join(alive_ips))
        print("Alive IP addresses saved to alive.txt")
    else:
        print("No alive IP addresses found within the specified CIDR range.")

def main():
    parser = argparse.ArgumentParser(description="CIDRProbe - Advanced CIDR Scanner")
    parser.add_argument("cidr", type=str, help="CIDR range to scan")
    parser.add_argument("-p", "--port", nargs="+", default=[], help="Port number(s) to check (optional)")
    parser.add_argument("-t", "--timeout", type=int, default=1, help="Timeout for HTTP requests (default: 1 second)")
    args = parser.parse_args()

    if not args.port:
        print("Please provide at least one port to scan.")
        return

    scan_cidr(args.cidr, args.port, args.timeout)

if __name__ == "__main__":
    # Print banner
    print(banner)

    # Execute the main function
    main()
