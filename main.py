import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def process_url(number, browser, xpaths):
    print(f"Processing symbol {number}...")
    url = f"https://www.tradingview.com/symbols/TADAWUL-{number}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, xpaths['primary'].format(1))))
        div_index = 1
        while True:
            primary_element_xpath = xpaths['primary'].format(div_index)
            try:
                element_html = browser.find_element(
                    By.XPATH, primary_element_xpath).get_attribute('outerHTML')
                process_element(element_html, number, output_data)
                div_index += 1
            except Exception:
                break
    except Exception as e:
        try:
            element_html = browser.find_element(
                By.XPATH, xpaths['secondary']).get_attribute('outerHTML')
            process_element(element_html, number, output_data)
        except Exception:
            pass

    return output_data

def process_element(element_html, number, output_data):
    soup = BeautifulSoup(element_html, 'html.parser')
    element_text = soup.get_text()
    pattern = r'(\d{1,2}/\d{1,2}/\d{4})|(\d+\.\d+)|(\w+)'
    matches = re.findall(pattern, element_text)
    flattened_matches = [item for sublist in matches for item in sublist if item]
    separated_text = ' '.join(flattened_matches)
    output_data.append([number, separated_text])

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

# Path to the input CSV file
csv_file_path = 'Symbols.csv'

# Path to the output CSV file
output_csv_file_path = 'OutputResults.csv'

# Read symbols from the CSV file
print("Reading symbols from the CSV file...")
symbols = []
try:
    with open(csv_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Skip the header if there is one
        symbols = [row[0] for row in csv_reader]
    print(f"Symbols loaded: {symbols}")
except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")

# Read the XPaths from the CSV file
xpath_file_path = 'xpath.csv'
xpaths = {}
try:
    with open(xpath_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) > 0:  # Check if the row is not empty
                xpaths[row[0]] = row[0]  # Use the first column for both key and value
    print(f"XPaths loaded: {xpaths}")
except FileNotFoundError:
    print(f"Error: File not found - {xpath_file_path}")

# Check if symbols were loaded
if not symbols:
    print("No symbols to process.")
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        for number in symbols:
            print(f"Processing symbol: {number}")
            data = process_url(number, browser, xpaths)
            if data:
                for row in data:
                    print(f"Writing to CSV: {row}")
                    csv_writer.writerow(row)
            else:
                print(f"No data found for symbol: {number}")

