import socket
import requests
import ipaddress
from termcolor import colored

def scan_cidr(cidr, port):
    ip_network = ipaddress.ip_network(cidr)

    print(colored(r'''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  ''', "white"))
    print(colored("contact me via telegram for any issues ", "white"))
    print(colored("https://t.me/brian_72", "white"))
    print()

    print(colored("IP                Port  -Status   HTTP -Status   Redirect Location", attrs=["bold"]))
    print("------------------------------------------------------------------")

    for ip in ip_network:
        ip_str = str(ip)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_str, int(port)))
            sock.close()

            if result == 0:
                port_status = colored("Open", "green")
            else:
                port_status = colored("Closed", "red")

            url = f"http://{ip_str}:{port}"
            try:
                response = requests.get(url, allow_redirects=False, timeout=3)

                if response.status_code == 302:
                    location = response.headers.get("Location")
                    if location:
                        redirect_location = colored(location, "cyan")
                    else:
                        redirect_location = colored("N/A", "cyan")
                    print(f"{ip_str:<17} {port:<6} {port_status:<8} {colored(response.status_code, 'blue'):<10} {redirect_location}")
                else:
                    print(f"{ip_str:<17} {port:<6} {port_status:<8} {colored(response.status_code, 'blue'):<10} {colored('N/A', 'cyan')}")

            except requests.exceptions.RequestException:
                print(f"{ip_str:<17} {port:<6} {port_status:<8} {colored('N/A', 'blue'):<10} {colored('N/A', 'cyan')}")

        except KeyboardInterrupt:
            print(colored("\nOperation cancelled by user.", "yellow"))
            break

def main():
    cidr = input("Enter the CIDR range: ")
    port = input("Enter the port to scan: ")

    scan_cidr(cidr, port)

if __name__ == "__main__":
    main()
