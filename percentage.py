import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to process each URL with dynamic XPaths
def process_url_dynamic(browser, symbol, xpaths):
    print(f"Processing symbol {symbol}...")
    url = xpaths[0].replace("{symbol}", symbol)
    browser.get(url)

    output_data = []

    try:
        # Wait for a known element that will be on the page once it's fully loaded
        wait_xpath = xpaths[1]
        WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, wait_xpath)))

        for xpath in xpaths[1:]:
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

# Read symbols and XPaths from the CSV file
csv_file_path = 'Symbols.csv'  # Update with your actual path to the CSV file
output_csv_file_path = 'OutputResults1.csv'  # Update with your desired output file path

symbols_and_xpaths = []
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            symbols_and_xpaths.append(row)
    print("Symbols and XPaths loaded.")
except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")
    browser.quit()
    exit()

# Check if data was loaded
if not symbols_and_xpaths:
    print("No data to process.")
    browser.quit()
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        # Write header row
        csv_writer.writerow(['Symbol'] + [f'Data {i}' for i in range(1, len(symbols_and_xpaths[0]))])

        # Process each symbol
        for row in symbols_and_xpaths:
            symbol = row[0]  # Assuming the first column contains the symbol
            xpaths = row
            data = process_url_dynamic(browser, symbol, xpaths)
            if data:
                csv_writer.writerow([symbol] + data)
                print(f"Data written for symbol {symbol}")
            else:
                print(f"No data found for symbol {symbol}")

# Close the browser after all symbols have been processed
browser.quit()
