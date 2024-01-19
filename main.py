import csv
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def process_url(browser, symbol, website_template, xpath_template, format_info):
    print(f"Processing symbol {symbol}...")
    formatted_website_url = website_template.format(number=symbol)
    print(f"Debug: Formatted website URL for symbol {symbol}: {formatted_website_url}")
    browser.get(formatted_website_url)

    output_data = []
    index = 1

    if '{}' in xpath_template:  # Check if the XPath template has a curly bracket
        while True:
            current_xpath = xpath_template.format(index)
            print(f"Debug: Formatted XPath for symbol {symbol} at index {index}: {current_xpath}")
            try:
                element = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.XPATH, current_xpath)))
                element_html = element.get_attribute('outerHTML')
                output_data.append(process_element(element_html, format_info))
                index += 1
            except Exception as e:
                print(f"Exception caught for symbol {symbol} at index {index}: {e}")
                break
    else:
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath_template)))
            element_html = element.get_attribute('outerHTML')
            output_data.append(process_element(element_html, format_info))
        except Exception as e:
            print(f"Exception caught for symbol {symbol}: {e}")

    return output_data


def process_element(element_html, format_info):
    soup = BeautifulSoup(element_html, 'html.parser')
    element_text = soup.get_text()
    print(f"Debug: Raw Element Text: {element_text}")

    if format_info:
        try:
            formatted_data = re.findall(format_info, element_text)
            print(f"Debug: Formatted Data: {formatted_data}")
            return formatted_data
        except Exception as e:
            print(f"Regex formatting error: {e}")
            return [element_text]  # Fallback to raw text
    else:
        return [element_text]

# Initialize Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")

# Initialize Selenium WebDriver
browser = webdriver.Chrome(options=chrome_options)

# Read symbols from the CSV file
symbols_csv_file_path = 'Symbols.csv'
symbols = []
try:
    with open(symbols_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Skip the header if there is one
        symbols = [row[0] for row in csv_reader]
    print(f"Symbols loaded: {symbols}")
except FileNotFoundError:
    print(f"Error: File not found - {symbols_csv_file_path}")
    browser.quit()

# Read the XPath CSV file
xpath_csv_file_path = 'xpath.csv'
xpaths_info = []
try:
    with open(xpath_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row
        for row in csv_reader:
            xpaths_info.append(row[:3])  # First three columns: website, xpath, formatting
    print(f"XPath info loaded: {xpaths_info}")
except FileNotFoundError:
    print(f"Error: File not found - {xpath_csv_file_path}")
    browser.quit()

# Check if symbols and XPath info were loaded
if not symbols or not xpaths_info:
    print("No symbols or XPath info to process.")
    browser.quit()
else:
    # Open the output CSV file for writing
    output_csv_file_path = 'OutputResults.csv'
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        # Process each symbol with each XPath template
        for symbol in symbols:
            for website_template, xpath_template, format_info in xpaths_info:
                data = process_url(browser, symbol, website_template, xpath_template, format_info)
                if data:
                    for element_text in data:
                        csv_writer.writerow([symbol] + element_text)
                        print(f"Data written for symbol {symbol}: {element_text}")
                else:
                    print(f"No data found for symbol {symbol} with {xpath_template}")

# Close the browser after all symbols have been processed
browser.quit()
