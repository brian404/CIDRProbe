import requests

# Function to fetch the Security Trails API key from the 'st_api.txt' file
def get_api_key():
    try:
        with open('st_api.txt', 'r') as file:
            api_key = file.read().strip()
            return api_key
    except FileNotFoundError:
        return None

# Function to perform Security Trails IP lookup
def perform_securitytrails_ip_lookup(ip_address):
    api_key = get_api_key()

    if not api_key:
        return ["Security Trails API key not available. Please add your API key to 'st_api.txt'."]

    try:
        url = f"https://api.securitytrails.com/v1/ip/{ip_address}"
        headers = {"APIKEY": api_key}
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            hostnames = data.get("hostnames", [])
            return hostnames
        else:
            return [f"Security Trails lookup failed with status code {response.status_code}"]
    except Exception as e:
        return [str(e)]
