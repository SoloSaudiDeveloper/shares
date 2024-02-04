from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    """Clean the text by removing non-printable characters."""
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    try:
        # Wait for the main content area to load
        container_xpath = '//*[@id="js-category-content"]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Extract titles
        titles_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj values-AtxjAQkN')]")
        titles = [sanitize(el.text) for el in titles_elements if el.text]

        # Extract parent elements and their children
        parents_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq values-AtxjAQkN')]")
        parents_data = []
        for parent in parents_elements:
            children = parent.find_elements(By.XPATH, ".//*[contains(@class, 'child-class-here')]")  # Update child class
            children_texts = [sanitize(child.text) for child in children if child.text]
            parents_data.append(children_texts)

        return titles, parents_data
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")
        return [], []

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

symbols = ['4344', '2222']  # Placeholder for actual symbols list
output_csv_file_path = 'OutputResults.csv'

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    for symbol in symbols:
        titles, parents_data = process_url_dynamic(browser, symbol)
        # Write titles (top row)
        csv_writer.writerow([symbol] + titles)
        # Write parents and children data
        for parent_data in parents_data:
            csv_writer.writerow([symbol] + parent_data)

        print(f"Data written for symbol {symbol}")

browser.quit()
