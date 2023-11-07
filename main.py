from tabulate import tabulate
import amazonScraper
import flipkartScraper

if __name__ == "__main__":
    # Prompt the user to enter URLs for both Amazon and Flipkart products
    amazon_url = input("Enter the Amazon product URL: ")
    flipkart_url = input("Enter the Flipkart product URL: ")

    print("Loading...")

    # Scrape product information from Amazon and Flipkart
    amazon_info = amazonScraper.scrape_amazon_product_info(amazon_url)
    flipkart_info = flipkartScraper.scrape_flipkart_product_info(flipkart_url)

    if amazon_info and flipkart_info:
        # Create a table combining data from Amazon and Flipkart
        combined_data = [
            ["Product  Name", amazon_info[0][1], flipkart_info[0][1]],
            ["Product  Price", amazon_info[1][1], flipkart_info[1][1]]
        ]

        headers = [" ", "Amazon", "Flipkart"]
        table = tabulate(combined_data, headers, tablefmt="pretty")

        print("Scraping successful:")
        print(table)
    else:
        print("Scraping failed.")
