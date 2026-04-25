# scraping logic
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def scrape_product(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()


