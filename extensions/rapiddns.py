import requests
from bs4 import BeautifulSoup

def reverse_ip_lookup(ip_address):
    url = f"https://rapiddns.io/sameip/{ip_address}#result"

    try:
        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            domain_elements = soup.find_all('td', class_='ellipsis')
            domains = [element.get_text() for element in domain_elements]
            return domains

        else:
            return None

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    ip_address = input("Enter the IP address for reverse lookup: ")

    result = reverse_ip_lookup(ip_address)
    if result:
        for domain in result:
            print(domain)
    else:
        print("Reverse lookup failed.")
