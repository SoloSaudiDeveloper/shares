from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    """Clean the text by removing non-printable characters."""
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    """Process each URL and extract data from elements with the specified class."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        # Wait for the page container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Find elements by class name within the container container-vKM0WfUu
        #container_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'container-OxVAcLqi')]")
        container_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'container-vKM0WfUu')]")
        # Extract and sanitize text from each element found
        for element in container_elements:
            sanitized_text = sanitize(element.text)
            output_data.append(sanitized_text)
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    # Concatenate all extracted data into a single string for the symbol
    return ' | '.join(output_data)

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

symbols = ['4344', '2222']  # Placeholder for actual symbols list
output_csv_file_path = 'OutputResults.csv'

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Data'])  # Write header row

    for symbol in symbols:
        consolidated_data = process_url_dynamic(browser, symbol)
        # Write symbol and consolidated data to a single row
        csv_writer.writerow([symbol, consolidated_data])
        print(f"Data written for symbol {symbol}")

browser.quit()
