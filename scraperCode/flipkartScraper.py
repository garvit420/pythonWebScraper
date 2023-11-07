from tabulate import tabulate
import requests
from bs4 import BeautifulSoup
import random

# List of user agents
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
]


# Function to scrape product information
def scrape_flipkart_product_info(product_url):
    while True:
        headers = ({
            'User-Agent': random.choice(user_agents),
            'Accept-Language': 'en-US, en;q=0.5'
        })

        try:
            response = requests.get(product_url, headers=headers)
            response.raise_for_status()  # Check for request success
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return

        soup = BeautifulSoup(response.text, 'html.parser')

        product_name_element = soup.find('span', {'class': 'B_NuCI'})
        product_price_element = soup.find('div', {'class': '_30jeq3 _16Jk6d'})

        if product_name_element and product_price_element:
            product_name = product_name_element.get_text().strip()
            product_price = product_price_element.get_text().strip()
            data = [
                ["Product Name", product_name[:35] + "..."],
                ["Product Price", product_price],
            ]
            return data
        else:
            print("not found prod")
            continue  # again request and find name and price


if __name__ == "__main__":
    # Prompt the user to enter a URL
    url = input("Enter the Flipkart product URL: ")

    print("Loading...")

    header = [" ", "Flipkart"]
    table = tabulate(scrape_flipkart_product_info(url), header, tablefmt="pretty")

    if table:
        print("Scraping successful:")
        print(table)
    else:
        print("Scraping failed.")
