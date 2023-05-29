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
            if nm[ip_str].has_tcp(port) and nm[ip_str]['tcp'][port]['state'] == 'open':
                status = colored("Open", "green")
            else:
                status = colored("Closed", "red")
            
            url = f"http://{ip_str}:{port}"
            response = requests.get(url, timeout=3)
            http_status = response.status_code
            if http_status == 200:
                http_status = colored(http_status, "green")
            else:
                http_status = colored(http_status, "yellow")
            
            print(f"{ip_str:<17} {port:<6} {status:<8} {http_status:<10}")
        
        except requests.exceptions.RequestException:
            print(f"{ip_str:<17} {port:<6} {status:<8} {'N/A':<10}")

def main():
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan: ")

    try:
        scan_cidr(cidr, port)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

if __name__ == "__main__":
    print('''
    IP                Port  -Status   HTTP -Status
    ----------------------------------------------
    ''')
    print("Use this banner and my Telegram link for contact purpose")
    print("https://t.me/brian_72")
    main()
