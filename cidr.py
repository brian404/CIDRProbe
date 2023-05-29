from termcolor import colored
import requests
import ipaddress
import nmap

def scan_cidr(cidr, port):
    ip_network = ipaddress.ip_network(cidr)
    nm = nmap.PortScanner()
    
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
                if response.status_code == 200:
                    http_status = colored(response.status_code, 'green')
                    http_message = colored('(OK)', 'yellow')
                else:
                    http_status = colored(response.status_code, 'green')
                    http_message = colored(f'({response.reason})', 'yellow')
            except requests.exceptions.RequestException:
                http_status = colored('Error', 'red')
                http_message = 'Connection Error'
            
            print(f"{colored(ip_str, 'white', attrs=['bold']):<15}{port:<7}{status:<13}{http_status:<10}{http_message}")
        
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            break

def main():
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan (default is 80): ") or '80'

    try:
        ip_network = ipaddress.ip_network(cidr)
        print(f"\nScanning CIDR range: {cidr}")
        print(f"Port: {port}\n")
        print("IP             Port   Status     HTTP Status     HTTP Response")
        print("----------------------------------------------------------------")
        scan_cidr(cidr, port)
    
    except ValueError:
        print("Invalid CIDR range input. Please enter a valid CIDR range.")

if __name__ == "__main__":
    print('''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  
https://t.me/brian_72
contact me via telegram for any issues
''')
    main()
