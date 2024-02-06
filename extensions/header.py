import requests

def check_header_info(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("URL:", url)
            print("IP Address:", response.headers.get('X-Forwarded-For', 'Not available'))
            print("Hostname:", response.headers.get('Server', 'Not available'))
        else:
            print("Failed to retrieve information. Status code:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))
