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
    """Process each URL and extract data from child elements grouped by their parent."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    titles_and_data = []  # To store both titles and children data

    try:
        # Wait for the page container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # First, find and process titles
        titles = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        for title in titles:
            titles_and_data.append([sanitize(title.text)])  # Each title in its own list as a single row

        # Then, find parent elements and their children
        parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")
        for parent in parents:
            children = parent.find_elements(By.XPATH, "./*")  # Adjust based on actual child tag structure
            child_texts = [sanitize(child.text) for child in children]
            titles_and_data.append(child_texts)  # Each group of children in its own list as a single row

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return titles_and_data

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

symbols = ['4344', '2222']  # Updated symbols list as per your request
output_csv_file_path = 'OutputResults.csv'

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)

    for symbol in symbols:
        titles_and_children = process_url_dynamic(browser, symbol)
        for row_data in titles_and_children:
            # Write symbol and row data to CSV, each in separate cells
            csv_writer.writerow([symbol] + row_data)
        print(f"Data written for symbol {symbol}")

browser.quit()
