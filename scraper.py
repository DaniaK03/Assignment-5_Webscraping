from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import pandas as pd
import time
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Uncomment if you want headless mode
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")

# Rotate User-Agent to prevent detection
ua = UserAgent()
options.add_argument(f"user-agent={ua.random}")

# Set up WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.ebay.com/globaldeals/tech"

def scrape_ebay_data():
    """Scrape eBay tech deals."""
    driver.get(url)
    time.sleep(5)  # Allow time for elements to load

    # Scroll down multiple times to load all products
    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    # Try to get all product elements
    try:
        products = WebDriverWait(driver, 15).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.dne-itemtile"))
        )
    except Exception as e:
        print(f"Error finding products: {e}")
        driver.quit()
        return []

    ebay_data_list = []

    for product in products:
        try:
            title = product.find_element(By.CLASS_NAME, "dne-itemtile-title").text
            price = product.find_element(By.CLASS_NAME, "dne-itemtile-price").text
            original_price_elem = product.find_elements(By.CLASS_NAME, "dne-itemtile-original-price")
            original_price = original_price_elem[0].text if original_price_elem else "N/A"
            shipping_elem = product.find_elements(By.CLASS_NAME, "dne-itemtile-delivery")
            shipping = shipping_elem[0].text if shipping_elem else "N/A"
            item_url = product.find_element(By.TAG_NAME, "a").get_attribute("href")
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            ebay_data_list.append({
                "timestamp": timestamp,
                "title": title,
                "price": price,
                "original_price": original_price,
                "shipping": shipping,
                "item_url": item_url,
            })

        except Exception as e:
            print(f"Error processing a product: {e}")
    
    return ebay_data_list

def save_to_csv(data_list):
    """Save scraped data to CSV."""
    file_name = "ebay_tech_deals.csv"
    
    try:
        df = pd.read_csv(file_name)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["timestamp", "title", "price", "original_price", "shipping", "item_url"])

    # Create a DataFrame for new data
    new_df = pd.DataFrame(data_list)

    # Concatenate with the existing DataFrame
    df = pd.concat([df, new_df], ignore_index=True)

    # Save back to CSV
    df.to_csv(file_name, index=False)

if __name__ == "__main__":
    print("Scraping eBay Tech Deals...")
    scraped_data = scrape_ebay_data()
    if scraped_data:
        save_to_csv(scraped_data)
        print("Data saved to ebay_tech_deals.csv")
    else:
        print("No data scraped.")
    
    driver.quit()
