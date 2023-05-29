import argparse
import ipaddress
import requests
from requests.exceptions import RequestException
from termcolor import colored

def scan_cidr(cidr, port):
    try:
        network = ipaddress.ip_network(cidr)
    except ValueError:
        print("Invalid CIDR range. Please provide a valid CIDR range.")
        return

    print(f"Scanning CIDR range: {cidr}")
    for ip in network.hosts():
        try:
            url = f"http://{ip}:{port}"
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                print(f"{ip} - {colored('[+]', 'green')} Status: {response.status_code}")
            else:
                print(f"{ip} - {colored('[-]', 'red')} Status: {response.status_code}")
        except RequestException:
            print(f"{ip} - {colored('[-]', 'red')} Failed to connect")

    print("Scan completed.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="CIDRProbe - Advanced CIDR Scanner")
    parser.add_argument("cidr", type=str, help="CIDR range to scan")
    parser.add_argument("-p", "--port", nargs="+", type=int, default=[80],
                        help="Port(s) to scan (default: 80)")
    return parser.parse_args()


def main():
    banner = r"""
  ____ ___ ____  ____  ____
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___
| |    | || | | | |_) | |_) | '__/ _ \
| |___ | || |_| |  _ <|  __/| | | (_) |
 \____|___|____/|_| \_\_|   |_|  \___/

CIDRProbe - Advanced CIDR Scanner
    """
    print(banner)

    args = parse_arguments()
    cidr = args.cidr
    ports = args.port

    for port in ports:
        scan_cidr(cidr, port)


if __name__ == "__main__":
    main()
