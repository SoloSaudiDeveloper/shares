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

    grouped_output_data = []

    try:
        # Wait for the page container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Find each container
        containers = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'container-OxVAcLqi')]")

        for container in containers:
            # For each container, find elements with values classes
            values_elements = container.find_elements(By.XPATH, ".//*[contains(@class, 'values-')]")
            container_data = []
            for element in values_elements:
                sanitized_text = sanitize(element.text)
                container_data.append(sanitized_text)
            grouped_output_data.append(container_data)
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return grouped_output_data

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

symbols = ['SYMBOL1', 'SYMBOL2']  # Placeholder for actual symbols list
output_csv_file_path = 'OutputResults.csv'

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    # No single header row, because data is grouped

    for symbol in symbols:
        grouped_data = process_url_dynamic(browser, symbol)
        for group in grouped_data:
            # Write symbol and each group of data to a new row
            csv_writer.writerow([symbol] + group)
        print(f"Data written for symbol {symbol}")

browser.quit()
