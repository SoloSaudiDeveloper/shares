import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sanitize(text):
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        # Wait for the container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Find all child elements under the container. Assuming these elements have a consistent tag or class to target.
        # Adjust the XPath to target the specific elements you're interested in.
        child_elements_xpath = f"{container_xpath}//*"  # This will select all elements under the container.
        child_elements = browser.find_elements(By.XPATH, child_elements_xpath)

        for element in child_elements:
            sanitized_text = sanitize(element.text)
            if sanitized_text:  # Ensure the text is not empty
                output_data.append(sanitized_text)

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")
    return output_data


# Initialize WebDriver with ChromeOptions
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Read symbols from CSV file
csv_file_path = 'Symbols.csv'
symbols = []
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        symbols = [row[0] for row in csv_reader if row]  # Ensure row is not empty
    print("Symbols loaded.")
except FileNotFoundError as e:
    print(f"Error: File not found - {csv_file_path}")
    print(e)
    browser.quit()
    exit()

# Process each symbol and write to CSV
output_csv_file_path = 'OutputResults.csv'  # Updated file name
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Data'])

    for symbol in symbols:
        data = process_url_dynamic(browser, symbol)
        for item in data:
            csv_writer.writerow([symbol, item])
        if not data:
            csv_writer.writerow([symbol, 'No data found'])
        print(f"Data written for symbol {symbol}")

browser.quit()
