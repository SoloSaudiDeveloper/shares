import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

def process_url(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://www.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []
    row_index = 1  # Start the row index at 1

    try:
        # Wait for some known element on the page to ensure the page has loaded
        WebDriverWait(browser, 20).until(
            EC.presence_of_element_located((By.XPATH, "Known element XPath")))

        while True:
            row_data = []
            for col_index in range(1, 6):  # Loop through columns 1 to 5
                current_xpath = f"//*[@id='js-category-content']/div[2]/div/div/div[8]/div[2]/div/div[1]/div[{row_index}]/div[{col_index}]"
                try:
                    element = browser.find_element_by_xpath(current_xpath)
                    row_data.append(element.text)
                except NoSuchElementException:
                    print(f"No more data found for symbol {symbol} at row {row_index}.")
                    break  # Exit the column loop if an element is not found

            if row_data:  # Check if any data was added for the row
                output_data.append(row_data)
                row_index += 1
            else:
                break  # Exit the row loop if no data was found for the current row
    except TimeoutException:
        print(f"Page did not load or element was not found for symbol {symbol}")

    return output_data

# Path to the input CSV file with symbols
symbols_csv_file_path = 'Symbols.csv'

# Path to the output CSV file
output_csv_file_path = 'OutputResults.csv'

# Initialize Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
# Initialize Selenium WebDriver
browser = webdriver.Chrome(options=chrome_options)

# Read symbols from the CSV file
print("Reading symbols from the CSV file...")
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
    exit()

# Check if symbols were loaded
if not symbols:
    print("No symbols to process.")
    browser.quit()
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        # Process each symbol
        for symbol in symbols:
            data = process_url(browser, symbol)
            if data:
                for row in data:
                    csv_writer.writerow([symbol] + row)
                print(f"Data written for symbol {symbol}: {data}")
            else:
                print(f"No data found for symbol {symbol}")

# Close the browser after all symbols have been processed
browser.quit()
