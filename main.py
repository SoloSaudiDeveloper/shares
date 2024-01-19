import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def process_url(browser, website, xpath_template):
    print(f"Processing website {website}...")
    browser.get(website)

    output_data = []
    index = 1  # Start the index at 1

    while True:
        current_xpath = xpath_template.format(index)
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, current_xpath)))
            element_html = element.get_attribute('outerHTML')
            output_data.append(process_element(element_html))
            index += 1
        except Exception as e:
            print(f"No more data found for website {website} at index {index}.")
            break

    return output_data

def process_element(element_html):
    soup = BeautifulSoup(element_html, 'html.parser')
    element_text = soup.get_text()
    return element_text

symbols_csv_file_path = 'Symbols.csv'
xpath_csv_file_path = 'xpath.csv'
output_csv_file_path = 'OutputResults.csv'

chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

print("Reading symbols from the CSV file...")
symbols = []
try:
    with open(symbols_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        symbols = [row[0] for row in csv_reader]
    print(f"Symbols loaded: {symbols}")
except FileNotFoundError:
    print(f"Error: File not found - {symbols_csv_file_path}")

try:
    with open(xpath_csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        xpath_data = [row for row in csv_reader if row]  # Reads only non-empty rows
    print(f"XPath data loaded.")
except FileNotFoundError:
    print(f"Error: File not found - {xpath_csv_file_path}")

if not symbols or not xpath_data:
    print("No symbols or XPath data to process.")
    browser.quit()
else:
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        for symbol in symbols:
            for row in xpath_data:
                website = row[0].format(number=symbol)
                xpath_template = row[1]
                data = process_url(browser, website, xpath_template)
                if data:
                    for element_text in data:
                        csv_writer.writerow([symbol, element_text])
                    print(f"Data written for symbol {symbol}: {element_text}")
                else:
                    print(f"No data found for symbol {symbol}")

browser.quit()
