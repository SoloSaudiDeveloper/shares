import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def process_url(browser, url_template, symbol, xpath):
    print(f"Processing symbol {symbol}...")
    url = url_template.format(number=symbol)
    browser.get(url)

    output_data = []
    index = 1

    while True:
        current_xpath = xpath.format(index)
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, current_xpath)))
            element_html = element.get_attribute('outerHTML')
            output_data.append(process_element(element_html))
            index += 1
        except Exception as e:
            print(f"No more data found for symbol {symbol} at index {index}.")
            break

    return output_data

def process_element(element_html):
    soup = BeautifulSoup(element_html, 'html.parser')
    element_text = soup.get_text()
    return element_text

# File paths
symbols_csv_file_path = 'Symbols.csv'
xpath_csv_file_path = 'xpath.csv'
output_csv_file_path = 'OutputResults.csv'

# Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

# Read symbols
print("Reading symbols from the CSV file...")
symbols = []
try:
    with open(symbols_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Skip header
        symbols = [row[0] for row in csv_reader]
    print(f"Symbols loaded: {symbols}")
except FileNotFoundError:
    print(f"Error: File not found - {symbols_csv_file_path}")

# Read XPath configurations
xpath_configs = []
try:
    with open(xpath_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            xpath_configs.append(row)  # Each row contains [url_template, xpath, ...comments]
    print("XPath configurations loaded.")
except FileNotFoundError:
    print(f"Error: File not found - {xpath_csv_file_path}")

# Check if symbols and XPath configurations were loaded
if not symbols or not xpath_configs:
    print("No symbols or XPath configurations to process.")
    browser.quit()
else:
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        for symbol in symbols:
            for config in xpath_configs:
                url_template, xpath = config[0], config[1]
                data = process_url(browser, url_template, symbol, xpath)
                if data:
                    for element_text in data:
                        csv_writer.writerow([symbol, element_text])
                    print(f"Data written for symbol {symbol}: {element_text}")
                else:
                    print(f"No data found for symbol {symbol}")

# Close browser
browser.quit()
