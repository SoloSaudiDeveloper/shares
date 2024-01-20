import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Hardcoded XPaths based on the provided Excel file
BASE_URL = "https://www.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
XPATHS = [
    "//*[@id='js-category-content']/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[3]/div[2]",
    "//*[@id='js-category-content']/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[3]",
    # Add additional XPaths here based on the Excel file
]

# Function to process each URL with the given XPaths
def process_url_dynamic(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = BASE_URL.format(symbol=symbol)
    browser.get(url)

    output_data = []

    try:
        # Wait for the page to load by checking for the presence of the first element
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, XPATHS[0])))

        # Extract data using the provided XPaths
        for xpath in XPATHS:
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

# Check if symbols were loaded
if not symbols:
    print("No symbols to process.")
    browser.quit()
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        # Write header row
        csv_writer.writerow(['Symbol'] + [f'Data {i + 1}' for i in range(len(XPATHS))])

        # Process each symbol
        for symbol in symbols:
            data = process_url_dynamic(browser, symbol)
            if data:
                csv_writer.writerow([symbol] + data)
                print(f"Data written for symbol {symbol}")
            else:
                print(f"No data found for symbol {symbol}")

# Close the browser after all symbols have been processed
browser.quit()
