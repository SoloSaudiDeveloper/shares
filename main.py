import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def process_url(number, browser, xpath):
    print(f"Processing symbol {number}...")
    url = f"https://www.tradingview.com/symbols/TADAWUL-{number}/financials-dividends/"
    browser.get(url)

    output_data = []

    div_index = 0  # Start from 0
    while True:
        formatted_xpath = xpath.replace('{loop}', str(div_index))
        try:
            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, formatted_xpath)))
            element_html = browser.find_element(By.XPATH, formatted_xpath).get_attribute('outerHTML')
            process_element(element_html, number, output_data)
            div_index += 1
        except Exception:
            break  # Exit the loop if no element is found or timeout occurs

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

# Read the first XPath from the CSV file
xpath_file_path = 'xpath.csv'
primary_xpath = ""
try:
    with open(xpath_file_path, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        primary_xpath = next(csv_reader)[0]  # Get the first row, first column
    print(f"Primary XPath loaded: {primary_xpath}")
except FileNotFoundError:
    print(f"Error: File not found - {xpath_file_path}")

# Check if symbols and primary_xpath were loaded
if not symbols or not primary_xpath:
    print("No symbols to process or no primary XPath found.")
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        for number in symbols:
            print(f"Processing symbol: {number}")
            data = process_url(number, browser, primary_xpath)
            if data:
                for row in data:
                    print(f"Writing to CSV: {row}")
                    csv_writer.writerow(row)
            else:
                print(f"No data found for symbol: {number}")
