import requests

def reverse_ip_lookup(ip_address):
    try:
        url = f"http://api.hackertarget.com/reverseiplookup/?q={ip_address}"
        print(f"Requesting URL: {url}")  # Debugging line
        response = requests.get(url)

        print(f"Response status code: {response.status_code}")  # my code is shit🙂// debug line

        if response.status_code == 200:
            hostnames = response.text.splitlines()
            return hostnames
        else:
            return [f"Hacker Target lookup failed with status code {response.status_code}"]

    except Exception as e:
        return [str(e)]

def get_hackertarget_results(ip_address):
    hostnames = reverse_ip_lookup(ip_address)
    return hostnames
