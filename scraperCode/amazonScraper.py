from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
import random

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 8_4_1 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12H321 Safari/600.1.4",
    "Mozilla/5.0 (compatible, MSIE 11, Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0;  Trident/5.0)",
    "Mozilla/5.0 (Windows; U; MSIE 7.0; Windows NT 6.0; en-US)",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]


# Function to scrape product information
def scrape_amazon_product_info(product_url):
    while True:
        headers = {
            'User-Agent': random.choice(user_agents),
        }

        try:
            response = requests.get(product_url, headers=headers)
            response.raise_for_status()  # Check for request success
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if CAPTCHA is present
        captcha_element = soup.find('p', {'class': 'a-last'})

        if captcha_element:
            continue  # Skip to the next iteration of the loop

        product_name_element = soup.find('span',
                                         {'class': 'a-size-large product-title-word-break'} or {'id': 'productTitle'})
        product_price_element = soup.find('span', {'class': 'a-price-whole'})
        product_price_symbol = soup.find('span', {'class': 'a-price-symbol'})

        if product_name_element and product_price_element:
            product_name = product_name_element.get_text().strip()
            price_symbol = product_price_symbol.get_text().strip()
            product_price = product_price_element.get_text().strip()[:-1]

            data = [
                ["Product Name", product_name[:35] + "..."],
                ["Product Price", price_symbol + product_price],
            ]
            return data
        else:
            continue  # again request and find name and price


if __name__ == "__main__":
    # Prompt the user to enter a URL
    url = input("Enter the Amazon product URL: ")

    print("Loading...")

    header = [" ", "Amazon"]
    table = tabulate(scrape_amazon_product_info(url), header, tablefmt="pretty")

    if table:
        print("Scraping successful:")
        print(table)
    else:
        print("Scraping failed.")
