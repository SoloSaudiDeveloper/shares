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
        # Wait for the page container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Find elements by class name within the container
        values_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-')]")

        # Extract and sanitize text from each element found
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

# Assuming 'symbols' list is already populated (replace 'Symbols.csv' with your actual CSV file path)
symbols = []  # Placeholder for symbols list
csv_file_path = 'Symbols.csv'  # Update with your actual CSV file path
output_csv_file_path = 'OutputResults.csv'  # Update with your desired output CSV file path

try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:  # Ensure the row is not empty
                symbols.append(row[0])
    print("Symbols loaded.")
except FileNotFoundError as e:
    print(f"Error: File not found - {csv_file_path}")
    print(e)
    browser.quit()
    exit()

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    # Assuming you may not know the exact number of data points beforehand, initialize with a large enough header
    # Adjust the range based on the maximum expected number of values per symbol
    headers = ['Symbol'] + [f'Value {i+1}' for i in range(20)]  # Example with 20 values
    csv_writer.writerow(headers)

    for symbol in symbols:
        data = process_url_dynamic(browser, symbol)
        # Ensure the row has the same number of columns as the header
        row = [symbol] + data + [''] * (len(headers) - 1 - len(data))
        csv_writer.writerow(row)
        print(f"Data written for symbol {symbol}")

browser.quit()
