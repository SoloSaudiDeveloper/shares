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

    try:
        # Wait for the container to be present
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Locate all elements with class 'values' within the container
        values_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[@class='values']")

        # Process each found element
        for element in values_elements:
            sanitized_text = sanitize(element.text)
            output_data.append(sanitized_text)
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Assuming 'symbols' list is already populated
symbols = ['4344', '2222']  # Example symbols list
output_csv_file_path = 'OutputResults.csv'  # Update to your desired path

# Process each symbol
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Data'])  # Write the header

    for symbol in symbols:
        data = process_url_dynamic(browser, symbol)
        # Write each value found for the symbol in a new row
        for value in data:
            csv_writer.writerow([symbol, value])
        print(f"Data written for symbol {symbol}")

browser.quit()
