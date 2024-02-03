from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    """Sanitize the text by removing non-printable characters."""
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    """Process each symbol URL and extract data from elements with class 'container-OxVAcLqi'."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        # Wait for the page to load and then find all 'container-OxVAcLqi' elements
        WebDriverWait(browser, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "container-OxVAcLqi"))
        )
        containers = browser.find_elements(By.CLASS_NAME, "container-OxVAcLqi")

        for container in containers:
            # Extract and sanitize the text from each container
            text = sanitize(container.text)
            output_data.append(text)
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data

# Setup Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--headless')  # Run in headless mode
chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
chrome_options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems
browser = webdriver.Chrome(options=chrome_options)

# Placeholder for symbols list; replace with actual reading from CSV
symbols = ['4344', '2222']  # Example symbols; replace with your list
output_csv_file_path = 'OutputResults.csv'  # Define your output CSV file path

# Process each symbol and output to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Container Text'])  # Writing header

    for symbol in symbols:
        container_texts = process_url_dynamic(browser, symbol)
        for text in container_texts:
            csv_writer.writerow([symbol, text])  # Write each container's text to the CSV
        print(f"Data written for symbol {symbol}")

browser.quit()
