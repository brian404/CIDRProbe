import ipaddress
import socket

def scan_cidr(cidr, port):
    ip_network = ipaddress.ip_network(cidr)
    print(f"Scanning CIDR range: {cidr}")
    print(f"Port: {port}\n")
    print("IP\t\tPort\tStatus")
    print("--------------------------------------")

    for ip in ip_network.hosts():
        ip_str = str(ip)
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)  # Set a timeout for the connection attempt
                result = sock.connect_ex((ip_str, port))
                if result == 0:
                    print(f"{ip_str}\t{port}\tOpen")
                else:
                    print(f"{ip_str}\t{port}\tClosed")
        except socket.error:
            print(f"{ip_str}\t{port}\tUnable to scan")

def main():
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan (default is 80): ") or 80
    port = int(port)

    scan_cidr(cidr, port)

if __name__ == "__main__":
    print(r'''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  
For any assistance, please feel free to contact me via Telegram:
Telegram: https://t.me/brian_72
''')
    main()
