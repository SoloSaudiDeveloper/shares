import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to process each URL with provided XPaths
def process_url_dynamic(browser, symbol, xpaths):
    print(f"Processing symbol {symbol}...")
    url = f"https://www.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        # Wait for a known element that will be on the page once it's fully loaded
        wait_xpath = xpaths[0]  # Use the first XPath for waiting
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, wait_xpath)))

        # Process each XPath
        for xpath in xpaths:
            try:
                element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                output_data.append(element.text)
            except TimeoutException:
                print(f"Timed out waiting for element with XPath: {xpath}.")
                break
    except TimeoutException as e:
        print(f"Page did not load or known element was not found for symbol {symbol}. Exception: {e}")

    return output_data

# Initialize Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")

# Initialize Selenium WebDriver
browser = webdriver.Chrome(options=chrome_options)

# Read symbols from the CSV file
csv_file_path = 'Symbols.csv'  # Update with your actual path to the CSV file
output_csv_file_path = 'OutputResults.csv'  # Update with your desired output file path

symbols = []
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        symbols = [row[0] for row in csv_reader if row]  # Read symbols, skip empty rows
    print("Symbols loaded.")
except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")
    browser.quit()
    exit()

# Hardcoded XPaths for each symbol
xpaths = [
    "//*[@id='js-category-content']/div[1]/div[1]/div/div/div/h2",
    # Add all other XPaths here in the same format
    # ...
]

# Check if symbols were loaded
if not symbols:
    print("No symbols to process.")
    browser.quit()
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        # Write header row
        header = ['Symbol'] + [f'Data {i+1}' for i in range(len(xpaths))]
        csv_writer.writerow(header)

        # Process each symbol
        for symbol in symbols:
            data = process_url_dynamic(browser, symbol, xpaths)
            if data:
                csv_writer.writerow([symbol] + data)
                print(f"Data written for symbol {symbol}")
            else:
                print(f"No data found for symbol {symbol}")

# Close the browser after all symbols have been processed
browser.quit()
