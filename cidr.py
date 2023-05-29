import sys
import requests

BANNER = '''
  ____ ___ ____  ____  ____            _    
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \\
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/

CIDR Probe - Scan CIDR Range

'''

def main():
    if len(sys.argv) < 2:
        print("Usage: python cidr.py <CIDR> [-p <port>]")
        print("Example: python cidr.py 10.0.0.0/24 -p 80")
        return

    cidr = sys.argv[1]
    port = 80

    if len(sys.argv) > 3 and sys.argv[2] == "-p":
        port = int(sys.argv[3])

    print(BANNER)
    print(f"Scanning CIDR range: {cidr}")
    print(f"Port: {port}\n")

    try:
        ips = cidr.split('/')[0]
        prefix = int(cidr.split('/')[1])
        start_ip = sum([int(x) << y for x, y in zip(ips.split('.'), [24, 16, 8, 0])])
        end_ip = start_ip + 2 ** (32 - prefix)
        for ip in range(start_ip, end_ip):
            ip_address = '.'.join([str(ip >> (y << 3) & 0xFF) for y in [3, 2, 1, 0]])
            url = f"http://{ip_address}:{port}"
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    print(f"[+] {ip_address} - Port {port}: Open")
                    print(f"Status Code: {response.status_code}")
                else:
                    print(f"[-] {ip_address} - Port {port}: Closed")
                    print(f"Status Code: {response.status_code}")
            except requests.exceptions.RequestException:
                print(f"[-] {ip_address} - Failed to connect")

    except KeyboardInterrupt:
        print("\n\nScan interrupted by user.")


if __name__ == "__main__":
    main()
