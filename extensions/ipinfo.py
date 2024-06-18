import requests

def reverse_ip_lookup(ip_address):
    try:
        url = f"https://ipinfo.io/{ip_address}/json"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            if 'hostname' in data:
                hostnames = [data['hostname']]
            else:
                hostnames = ["No hostnames found"]
            return hostnames
        else:
            return [f"IPinfo.io lookup failed with status code {response.status_code}"]

    except Exception as e:
        return [str(e)]

def get_hackertarget_results(ip_address):
    hostnames = reverse_ip_lookup(ip_address)
    return hostnames
