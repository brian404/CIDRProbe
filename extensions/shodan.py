import requests

SERVER_ENDPOINT = "http://endpoint.brian72.eu.org:5000"

def get_shodan_api_key():
    try:
        response = requests.get(f"{SERVER_ENDPOINT}?api_name=shodan")
        if response.status_code == 200:
            data = response.json()
            return data.get("api_key")
        else:
            print(f"Failed to fetch Shodan API key. Status Code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

shodan_api_key = get_shodan_api_key()
if shodan_api_key:
    print(f"Using Shodan API key: {shodan_api_key}")
    # Perform your Shodan queries here
else:
    print("Shodan API key not available.")
