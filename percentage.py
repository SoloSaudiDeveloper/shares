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

    try:
        # Wait for the main content area to load
        main_content_xpath = '//*[@id="js-category-content"]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, main_content_xpath)))

        # Find elements with class 'container-OxVAcLqi'
        container_elements = browser.find_elements(By.XPATH, f"{main_content_xpath}//div[contains(@class, 'container-OxVAcLqi')]")

        # Concatenate text from all found container elements
        concatenated_text = ' | '.join(sanitize(element.text) for element in container_elements)
        
        return concatenated_text
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")
        return ''

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Load symbols from your CSV file
symbols = []  # Placeholder for symbols list
csv_file_path = 'Symbols.csv'  # Path to your CSV file containing symbols
output_csv_file_path = 'OutputResults.csv'  # Desired output CSV file path

# Read symbols from CSV file
try:
    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
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

# Process each symbol and write concatenated data to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Data'])  # Write header

    for symbol in symbols:
        concatenated_data = process_url_dynamic(browser, symbol)
        csv_writer.writerow([symbol, concatenated_data])
        print(f"Data written for symbol {symbol}")

browser.quit()
