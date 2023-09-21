import ipaddress
import ping3
from termcolor import colored
import socket
import subprocess
import ssl
import argparse

def get_http_status(ip_str, port):
    try:
        cmd = ["curl", "-i", f"{ip_str}:{port}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        output = result.stdout
        if "HTTP/1.1" in output:
            status_line = output.splitlines()[0]
            status_code = status_line.split()[1]
            return status_code
        else:
            return colored("N/A", "yellow")
    except subprocess.TimeoutExpired:
        return colored("Timeout", "red")
    except Exception:
        return colored("N/A", "yellow")

def check_ssl(ip_str, port):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip_str, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=ip_str) as ssock:
                tls_version = ssock.version()
                return f"Established TLS {tls_version}"
    except ssl.SSLError:
        return colored("SSL Handshake Failed", "red")
    except (socket.timeout, ConnectionRefusedError):
        return colored("N/A", "yellow")
    except Exception:
        return colored("N/A", "yellow")

def save_results_to_file(results):
    try:
        file_name = input("Do you want to save the scan results to a file? (Enter file name or press Enter to skip): ")
        if file_name:
            with open(file_name, "w") as file:
                file.writelines(results)
                print(f"Scan results saved to {file_name}")
    except Exception as e:
        print(f"Error saving scan results: {str(e)}")

def scan_cidr(cidr, port, ssl_check):
    try:
        ip_network = ipaddress.ip_network(cidr)
    except ValueError:
        print(colored("Invalid CIDR range. Please enter a valid range.", "red"))
        print(colored("Example: 192.168.0.0/24", "yellow"))
        return

    print(colored(r'''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  ''', "white"))
    print(colored("Contact me via Telegram for any issues.", "green"))
    print(colored("https://t.me/brian_72", "white"))
    print()

    if ssl_check:
        print(colored("IP                Status", "blue"), colored("Hostname", "cyan"), colored("HTTP Status", "green", attrs=["bold"]), colored("SSL/TLS", "magenta", attrs=["bold"]))
    else:
        print(colored("IP                Status", "blue"), colored("Hostname", "cyan"), colored("HTTP Status", "green", attrs=["bold"]))
    print("----------------------------------------------------------------------------------------")

    results = []

    try:
        for ip in ip_network.hosts():
            ip_str = str(ip)
            try:
                response_time = ping3.ping(ip_str)
                if response_time is not None:
                    status = colored("Alive", "green")
                else:
                    status = colored("Not Responding", "red")

                try:
                    hostname, _, _ = socket.gethostbyaddr(ip_str)
                except socket.herror:
                    hostname = colored("N/A", "yellow")

                http_status = get_http_status(ip_str, port)

                if ssl_check:
                    tls_info = check_ssl(ip_str, port)
                    if "SSL Handshake Failed" in tls_info:
                        tls_info = colored("SSL Not Found", "red")
                    results.append(f"{ip_str:<17} {status:<10} {hostname:<15} {http_status:<10} {tls_info}\n")
                    print(f"{colored(ip_str, 'blue'):<17} {status:<10} {colored(hostname, 'cyan'):<15} {colored(http_status, 'green', attrs=['bold'])} {colored(tls_info, 'magenta', attrs=['bold'])}")
                else:
                    results.append(f"{ip_str:<17} {status:<10} {hostname:<15} {http_status:<10}\n")
                    print(f"{colored(ip_str, 'blue'):<17} {status:<10} {colored(hostname, 'cyan'):<15} {colored(http_status, 'green', attrs=['bold'])}")

            except KeyboardInterrupt:
                print(colored("\nOperation cancelled by user.", "yellow"))
                break
    except KeyboardInterrupt:
        print(colored("\nOperation cancelled by user.", "yellow"))

    save_results_to_file(results)

def main():
    parser = argparse.ArgumentParser(description="CIDRProbe - IP Range Scanner")
    parser.add_argument("cidr", help="CIDR Range (e.g., 192.168.0.0/24)")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port to use for HTTP checks (default: 80)")
    parser.add_argument("-ssl", action="store_true", help="Perform SSL/TLS checks")

    args = parser.parse_args()
    scan_cidr(args.cidr, args.port, args.ssl)

if __name__ == "__main__":
    main()
