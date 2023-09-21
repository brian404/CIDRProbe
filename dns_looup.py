import requests

SERVER_URL = "http://endpoint.brian72.eu.org:5000"

def get_api_key(api_name):
    response = requests.get(f"{SERVER_URL}/get_api_key", params={"api_name": api_name})
    if response.status_code == 200:
        data = response.json()
        return data.get("api_key")
    else:
        print("Error fetching API key.")
        return None

# Function to perform DNS lookup using Hacker Target
def perform_hacker_target_lookup(ip_address, hacker_target_api_key):
    url = f"{SERVER_URL}/hacker_target_lookup?ip_address={ip_address}"
    response = requests.get(url)

    if response.status_code == 200:
        hostnames = response.json().get("result")
        print("Hacker Target - Hostnames:")
        for hostname in hostnames:
            print(hostname)
    else:
        print("Hacker Target - Error:", response.status_code)

# Function to perform DNS lookup using Shodan
def perform_shodan_lookup(ip_address, shodan_api_key):
    import shodan

    api = shodan.Shodan(shodan_api_key)

    try:
        # Perform Shodan DNS resolve query
        hostnames = api.dns.resolve(ip_address)
        print("Shodan - Hostnames:")
        for hostname in hostnames:
            print(hostname)

    except shodan.APIError as e:
        print("Shodan - Error:", str(e))

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Perform DNS lookup for an IP address.")
    parser.add_argument("ip_address", help="Specify the IP address to look up.")
    parser.add_argument("--services", nargs="+", choices=["hacker_target", "shodan"], default=["hacker_target"], help="Specify which services to use (hacker_target, shodan).")

    args = parser.parse_args()

    hacker_target_api_key = get_api_key("hacker_target")
    shodan_api_key = get_api_key("shodan")

    if "hacker_target" in args.services:
        perform_hacker_target_lookup(args.ip_address, hacker_target_api_key)

    if "shodan" in args.services:
        perform_shodan_lookup(args.ip_address, shodan_api_key)