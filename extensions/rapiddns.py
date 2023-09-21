import requests
import bs4

def reverse_ip_lookup(ip_address):
    # rapiddns -> TABLE -> scraping 'td'
    url = f"https://rapiddns.io/sameip/{ip_address}#result"

    try:
        resp = requests.get(url, timeout=5).text
        soup = bs4.BeautifulSoup(resp, "html.parser")

        result = []
        for item in soup.find_all("td"):
            subdomain = item.text
            if subdomain.endswith(ip_address):
                result.append(subdomain)

        return result

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    ip_address = input("Enter the IP address for reverse lookup: ")

    result = reverse_ip_lookup(ip_address)
    if result:
        for subdomain in result:
            print(subdomain)
    else:
        print("Reverse lookup failed.")
