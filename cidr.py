from termcolor import colored
import requests
import ipaddress
import nmap

def scan_cidr(cidr, port):
    ip_network = ipaddress.ip_network(cidr)
    nm = nmap.PortScanner()
    
    print("IP                Port   Status      HTTP Status")
    print("------------------------------------------------")
    
    try:
        for ip in ip_network.hosts():
            ip_str = str(ip)
            
            try:
                nm.scan(ip_str, arguments=f"-p {port}")
                if nm[ip_str].has_tcp(int(port)) and nm[ip_str]['tcp'][int(port)]['state'] == 'open':
                    status = colored('Open', 'green')
                else:
                    status = colored('Closed', 'blue')
                
                try:
                    response = requests.get(f"http://{ip_str}:{port}", timeout=2)
                    http_status = colored(response.status_code, 'green')
                    print(f"{ip_str:<18}{port:<6}{status:<12}{http_status}")
                    
                except requests.exceptions.RequestException:
                    print(f"{ip_str:<18}{port:<6}{status:<12}N/A")
                    
            except nmap.PortScannerError:
                print(f"{ip_str:<18}{port:<6}N/A{'N/A'}")
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
            
def main():
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan: ")
    
    scan_cidr(cidr, port)

if __name__ == "__main__":
    print('''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \\
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  
https://t.me/brian_72
contact me via telegram for any issues
''')
    main()
