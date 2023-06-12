import socket
import ipaddress
from termcolor import colored

def scan_ip_range(ip_range, port):
    try:
        network = ipaddress.ip_network(ip_range)
    except ValueError:
        print(colored("Invalid IP range. Please enter a valid range.", "red"))
        print(colored("Example: 162.159.129.0/24", "yellow"))
        return

    try:
        int_port = int(port)
        if int_port < 1 or int_port > 65535:
            raise ValueError
    except ValueError:
        print(colored("Invalid port number. Please enter a valid port.", "red"))
        print(colored("Example: 80", "yellow"))
        return

    print(colored("IP                Port  -Status   Hostname", attrs=["bold"]))
    print("------------------------------------------------")

    for ip in network.hosts():
        ip_str = str(ip)

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((ip_str, int_port))
            sock.close()

            if result == 0:
                port_status = colored("Open", "green")
            else:
                port_status = colored("Closed", "red")

            try:
                hostname = socket.gethostbyaddr(ip_str)[0]
            except socket.herror:
                hostname = "N/A"

            print(f"{ip_str:<17} {port:<6} {port_status:<8} {hostname}")
        except KeyboardInterrupt:
            print(colored("\nOperation cancelled by user.", "yellow"))
            break

def main():
    print("IP Range Scanner")
    print()

    print("Usage Example:")
    print("IP Range: 162.159.129.0/24")
    print("Port: 80")
    print()

    ip_range = input("Enter the IP range: ")
    port = input("Enter the port to scan: ")

    scan_ip_range(ip_range, port)

if __name__ == "__main__":
    main()