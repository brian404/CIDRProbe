from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def reverse_ip_lookup_selenium(ip_address):
    url = f"https://rapiddns.io/sameip/{ip_address}#result"

    try:
        # Set up the WebDriver (download the appropriate WebDriver for your browser)
        driver = webdriver.Chrome()  # Example for Chrome; adjust as needed

        # Open the URL
        driver.get(url)

        # Wait for the data to load (adjust the timeout as needed)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'ellipsis')))

        # Extract the domain names
        domain_elements = driver.find_elements(By.CLASS_NAME, 'ellipsis')
        domains = [element.text for element in domain_elements]

        return domains

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

    finally:
        # Close the WebDriver when done
        driver.quit()

if __name__ == "__main__":
    ip_address = input("Enter the IP address for reverse lookup: ")

    result = reverse_ip_lookup_selenium(ip_address)
    if result:
        for domain in result:
            print(domain)
    else:
        print("Reverse lookup failed.")
