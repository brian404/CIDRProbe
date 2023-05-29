from termcolor import colored
import requests
import ipaddress
import nmap

def scan_cidr(cidr, port):
    ip_network = ipaddress.ip_network(cidr)
    nm = nmap.PortScanner()

    print("IP                Port  -Status   HTTP -Status")
    print("----------------------------------------------")

    for ip in ip_network:
        ip_str = str(ip)
        try:
            if nm[ip_str].has_tcp(int(port)) and nm[ip_str]['tcp'][int(port)]['state'] == 'open':
                port_status = colored("Open", "green")
            else:
                port_status = colored("Closed", "red")

            url = f"http://{ip_str}:{port}"
            try:
                response = requests.get(url, timeout=3)
                http_status = response.status_code
                if http_status == 200:
                    http_status = colored(http_status, "green")
                else:
                    http_status = colored(http_status, "yellow")
                print(f"{ip_str:<17} {port:<6} {port_status:<8} {http_status:<10}")
            except requests.exceptions.RequestException:
                print(f"{ip_str:<17} {port:<6} {port_status:<8} {'N/A':<10}")

        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break

def main():
    print('''
 ____ ___ ____  ____  ____            _          
/ ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  
    ''')
    print("Use this banner and my Telegram link for contact purpose")
    print("https://t.me/brian_72")

    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan: ")

    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
