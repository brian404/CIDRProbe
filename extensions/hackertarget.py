import argparse
import requests

def reverse_ip_lookup(ip_address):
    try:
        url = f"http://api.hackertarget.com/reverseiplookup/?q={ip_address}"
        response = requests.get(url)

        if response.status_code == 200:
            hostnames = response.text.splitlines()
            return hostnames
        else:
            return ["Hacker Target lookup failed"]
    except Exception as e:
        return [str(e)]

def main():
    parser = argparse.ArgumentParser(description="Perform reverse IP lookup on domains using Hacker Target API")
    parser.add_argument("-ip", required=True, help="IP address to lookup")
    args = parser.parse_args()

    ip_address = args.ip
    hostnames = reverse_ip_lookup(ip_address)

    for hostname in hostnames:
        print(hostname)

if __name__ == "__main__":
    main()
