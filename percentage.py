from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    # Attempt to wait for the container to load with a longer timeout
    container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
    try:
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, container_xpath)))
        print("Container element found.")
        
        # Find all relevant child elements within the container
        elements = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'dividendRow')]")
        if not elements:
            print("No child elements found. Check XPath.")
        for element in elements:
            sanitized_text = sanitize(element.text)
            output_data.append(sanitized_text)

    except TimeoutException as e:
        print(f"Timed out waiting for container element. Error: {e}")

    return output_data
# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Assume 'symbols' list is already populated
symbols = ['4344', '1211']  # Example symbols list
output_csv_file_path = 'output_data.csv'

# Process each symbol
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Data'])  # Writing header

    for symbol in symbols:
        data = process_url_dynamic(browser, symbol)
        for row in data:
            csv_writer.writerow([symbol, row])
        print(f"Data written for symbol {symbol}")

browser.quit()
