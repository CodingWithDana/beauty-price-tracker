# beauty-price-tracker
A Python-based script helps find where to buy a beauty product at the best price online .

## Intentions
- Buying skincare and cosmetic products online often means checking multiple websites to find the best price.
- This tracker automates that process by:
  - Searching for a specific product across different online stores
  - Extracting product names, prices, and links
  - Comparing results to identify the best deal
- The goal is to save time and make smarter purchasing decisions.

## Tech Stack
- **Python**
- **Requests** (for sending HTTP requests)
- **BeautifulSoup** (for parsing HTML content)
- **(Future) Selenium / Playwright** (for handling dynamic websites)
- **(Optional) Pandas** (for data handling and analysis)

## How it works
1. A list of product URLs (or search results) is defined
2. The script sends requests to each webpage
3. HTML content is parsed using BeautifulSoup
4. Relevant data is extracted:
   - Product name
   - Price
   - Product link
5. Prices are cleaned and converted into comparable values
6. The script identifies and returns the cheapest option

## Features
- Scrapes product data from multiple websites
- Compares prices across different sources
- Outputs the best available deal
- Simple and extendable Python script

## Future Improvements
- Email notifications when:
  - A product drops below a target price
  - A watched product changes price
- Watchlist feature for tracking multiple products
- Support for more websites
- Smarter matching (same product, different naming formats)

## Notes
- This tracker is for learning purposes
- Some websites may block automated requests
