# scraping logic
import requests
import re
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

URL_MECCA = "https://www.mecca.com/en-au/estee-lauder/advanced-night-repair-synchronized-multi-recovery-complex-50ml-I-047179/?cgpath=search-results"
URL_ADORE = "https://www.adorebeauty.com.au/p/estee-lauder/estee-lauder-advanced-night-repair-synchronized-multi-recovery-complex-50ml.html"
URL_MYER = "https://www.myer.com.au/p/estee-lauder-advanced-night-repair-synchronized-multi-recovery-complex-serum?size=50ml"

# Mecca site
def scrape_mecca(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup_mecca = BeautifulSoup(response.text, "html.parser")
    # print(soup_mecca)

    # find the product name
    product_tag = soup_mecca.select_one('[data-testid="product-name"]')
    # extract clean text (strip=True removes extra spaces/new lines)
    product = product_tag.get_text(strip=True)
    # print(f"♡ Product Name: {product}")
    # find the price
    price_tag = soup_mecca.select_one('[data-testid="product-price"]')
    price = price_tag.get_text(strip=True)
    # print(f"★ Price: {price}")
    
    return {
        "store": "Mecca",
        "product": product,
        "price": price,
        "url": URL_MECCA
    }

# Adore Beauty site
def scrape_adore(url):
    response = requests.get(url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup_adore = BeautifulSoup(response.text, "html.parser")

    # find the product name
    # product_tag = soup_adore.select_one('[class="text-[28px] text-[#404040]"]')
    product_tag = soup_adore.select_one('.text-\\[28px\\]')
    if not product_tag:
        print("Product not found")
        return None
    
    # extract clean text (strip=True removes extra spaces/new lines)
    product = product_tag.get_text(strip=True)
    # find the price
    price_tag = soup_adore.select_one('[class="text-[25px] font-medium text-[#E15070]"]')
    price_tag = soup_adore.select_one('.text-\\[25px\\]')
    if not price_tag:
        print("Price not found")
        return None
    price = price_tag.get_text(strip=True)
    
    return {
        "store": "Adore",
        "product": product,
        "price": price,
        "url": URL_ADORE 
    }



# Myer site 
def scrape_myer(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        
        html = page.content()
        browser.close()

    soup_myer = BeautifulSoup(html, "html.parser") 

    product_tag = soup_myer.select_one('[data-cs-override-id="product-title"]')
    if not product_tag:
        print("Product name not found")
        return
    product = product_tag.get_text(strip=True)

    # get the price text near the product title, not the entire page
    price_section = product_tag.find_parent()
    nearby_text = price_section.get_text("\n", strip=True) if price_section else soup_myer.get_text("\n", strip=True)
    prices_as_text = re.findall(r"\$\d+(?:\.\d{2})?", nearby_text)
    if prices_as_text:
        prices_as_text
    else:
        return

    return {
        "store": "Myer",
        "product": product,
        "price": prices_as_text[0],
        "url": URL_MYER        
    }


# clean the scraped prices
def parse_price(price_text):
    try:
        cleaned = price_text.replace("$", "").replace(",", "").strip()
        return float(cleaned)
    except (ValueError, AttributeError):
        return None

# write comparision logic to get the lowest price
def find_best_price(stores):
    valid_stores = []
    
    for store in stores:
        if store and store.get("price"):
            store["price_number"] = parse_price(store["price"])
            valid_stores.append(store)
            
    if not valid_stores:
        print("Price not found")
        return None
    
    cheapest = min(valid_stores, key=lambda store: store["price_number"])
    
    print("Here are the snapshot of prices for the product from Mecca, Adore and Myer")

    for store in valid_stores:
        print(f"{store['store']}: {store['price']}")
    
    print(
        f"Currently {cheapest['store']} offers the best price"
        f" at {cheapest['price']}. Link to buy here: {cheapest['url']}"
    )
    
    return cheapest

result_mecca = scrape_mecca(URL_MECCA)
result_adore = scrape_adore(URL_ADORE)
result_myer = scrape_myer(URL_MYER)
stores = [result_mecca, result_adore, result_myer]
best_price = find_best_price(stores)

# Debug
# print(result_mecca)
# print(result_adore)
# print(result_myer)
