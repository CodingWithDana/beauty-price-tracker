# scraping logic
import requests
from bs4 import BeautifulSoup

url = "https://www.mecca.com/en-au/rhode/peptide-lip-tint-nourishing-glaze-raspberry-jelly-I-079509/?cgpath=brands-rhode"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_product(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # print(soup)

    # find the product name
    product_tag = soup.select_one('[data-testid="product-name"]')
    # extract clean text (strip=True removes extra spaces/new lines)
    product = product_tag.get_text(strip=True)
    print(product)
    # find the price
    price_tag = soup.select_one('[data-testid="product-price"]')
    price = price_tag.get_text(strip=True)
    print(price)
    
scrape_product(url)

#     # # return a dict
#     # return {
#     #     "name": name,
#     #     "price": price,
#     #     "url": url
#     # }

