from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import os
import time

def scrape_amazon_search_results(search_url, save_path=""):
    # Setup headless Chrome
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = webdriver.Chrome(options=options)

    print("⏳ Loading page...")
    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Product cards
    product_cards = soup.select('div.s-main-slot div.s-result-item[data-component-type="s-search-result"]')
    data = []

    for product in product_cards:
        # Extract product URL (the link to the product page)
        url_tag = product.select_one('h2 a')
        product_url = "https://www.amazon.com" + url_tag.get('href') if url_tag else "N/A"

        # Get product name and vendor from the search result
        title_tag = product.select_one('h2 a span')
        vendor_tag = product.select_one('div.a-row.a-size-base.a-color-secondary span.a-size-base')

        # Extract values, default to "N/A" if not found
        name = title_tag.get_text(strip=True) if title_tag else "N/A"
        vendor = vendor_tag.get_text(strip=True) if vendor_tag else "N/A"

        # Get the price (can be inside <span> with a class like "a-price-whole")
        price_tag = product.select_one('span.a-price > span.a-offscreen')
        price = price_tag.get_text(strip=True).replace("£", "").replace("$", "") if price_tag else "N/A"

        # Add the data to the list
        data.append({
            "name": name,
            "price": price,
            "vendor": vendor,
            "product_url": product_url
        })

    driver.quit()

    # Now, go to each product URL to extract detailed name and vendor (if needed)
    for entry in data:
        product_url = entry['product_url']
        if product_url != "N/A":
            driver = webdriver.Chrome(options=options)
            driver.get(product_url)
            time.sleep(3)

            # Scrape the product page for more detailed name and vendor
            page_soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract name and vendor on the product page
            product_name = page_soup.select_one('span#productTitle')
            product_vendor = page_soup.select_one('a#bylineInfo')
            
            # Update the data with the product's detailed information
            entry['name'] = product_name.get_text(strip=True) if product_name else entry['name']
            entry['vendor'] = product_vendor.get_text(strip=True) if product_vendor else entry['vendor']
            
            driver.quit()

    return pd.DataFrame(data)

# === Run Script ===
if __name__ == "__main__":
    search_url = input("🔍 Paste Amazon search URL: ").strip()
    save_path = input("📁 Folder to save CSV (or press Enter for current folder): ").strip()

    df = scrape_amazon_search_results(search_url, save_path)

    print(f"\n{df.head()}")

    # Save the data to CSV
    filename = f"{save_path}/amazon_search_results.csv"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    if not df.empty:
        df.to_csv(filename, index=False)
        print(f"\n✅ {len(df)} products saved to: {filename}")
    else:
        print("⚠️ No products found.")