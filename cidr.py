import ipaddress
import ping3
from termcolor import colored
import socket
import subprocess
import ssl
import argparse
from extensions import hackertarget
import concurrent.futures
import sys
import argparse
import concurrent.futures
from extensions import header

def get_http_status(ip_str):
    try:
        cmd = ["curl", "-i", ip_str]
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

def check_ssl(ip_str):
    try:
        context = ssl.create_default_context()
        with socket.create_connection((ip_str, 443), timeout=5) as sock:
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

def print_banner():
    print(colored(r'''
  ____ ___ ____  ____  ____            _          
 / ___|_ _|  _ \|  _ \|  _ \ _ __ ___ | |__   ___ 
| |    | || | | | |_) | |_) | '__/ _ \| '_ \ / _ \
| |___ | || |_| |  _ <|  __/| | | (_) | |_) |  __/
 \____|___|____/|_| \_\_|   |_|  \___/|_.__/ \___|
                                                  ''', "cyan"))
    print(colored("Contact me for any issues on Telegram:", "magenta"))
    print(colored("https://t.me/brian_72", "magenta"))
    print()

def check_http_and_ssl(ip_str, port, ssl_check):
    try:
        status = "Alive" if ping3.ping(ip_str) is not None else colored("Not Responding", "red")

        try:
            hostname, _, _ = socket.gethostbyaddr(ip_str)
        except socket.herror:
            hostname = colored("N/A", "yellow")

        http_status = colored(get_http_status(ip_str), "green", attrs=["bold"])
        tls_info = colored(check_ssl(ip_str), "magenta", attrs=["bold"]) if ssl_check else colored("N/A", "yellow")

        return f"{colored(ip_str, 'blue'):<17} {status:<10} {colored(hostname, 'cyan'):<15} {http_status:<10} {tls_info}\n"

    except concurrent.futures.TimeoutError:
        return f"{colored(ip_str, 'blue'):<17} {colored('Timeout', 'red')}\n"

    except Exception as e:
        return f"{colored(ip_str, 'blue'):<17} {colored('Error', 'red')}: {str(e)}\n"

def scan_cidr_parallel(cidr, port, ssl_check, use_hackertarget, use_securitytrails, header_check):
    try:
        ip_network = ipaddress.ip_network(cidr)
    except ValueError:
        print(colored("Invalid CIDR range. Please enter a valid range.", "red"))
        print(colored("Example: 192.168.0.0/24", "yellow"))
        return

    print_banner()

    if ssl_check:
        print(colored("IP                Status", "blue"), colored("Hostname", "cyan"), colored("HTTP Status", "green", attrs=["bold"]), colored("SSL/TLS", "magenta", attrs=["bold"]))
    else:
        print(colored("IP                Status", "blue"), colored("Hostname", "cyan"), colored("HTTP Status", "green", attrs=["bold"]))
    print("----------------------------------------------------------------------------------------")

    results = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(check_http_and_ssl, str(ip), port, ssl_check): ip for ip in ip_network.hosts()}

        for future in concurrent.futures.as_completed(futures):
            try:
                result = future.result()
                results.append(result)
                # Print or process the result as needed
                print(result)
            except Exception as e:
                print(f"Error processing result: {str(e)}")

    save_results_to_file(results)

def main():
    parser = argparse.ArgumentParser(description="CIDRProbe - IP Range Scanner")
    parser.add_argument("cidr", nargs="?", default=None, help="CIDR Range (e.g., 192.168.0.0/24)")
    parser.add_argument("-p", "--port", type=int, default=80, help="Port to use for HTTP checks (default: 80)")
    parser.add_argument("-ssl", action="store_true", help="Perform SSL/TLS checks")
    parser.add_argument("-ht", "--hackertarget", action="store_true", help="Use Hacker Target extension")
    parser.add_argument("-st", "--securitytrails", action="store_true", help="Use Security Trails extension")
    parser.add_argument("-H", "--header", action="store_true", help="Check header information")

    args = parser.parse_args()

    if args.cidr is None:
        args.cidr = input("Enter the CIDR range (e.g., 192.168.0.0/24): ")

    scan_cidr_parallel(args.cidr, args.port, args.ssl, args.hackertarget, args.securitytrails, args.header)

if __name__ == "__main__":
    main()
