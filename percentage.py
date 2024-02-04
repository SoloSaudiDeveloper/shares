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
    """Process each URL and extract data from specified classes and their child elements."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        # Wait for the page container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Extract Title Column Texts
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'titleColumn-C9MdAMrq')]")
        for title_column in title_columns[:3]:  # Only process the first 3
            title_text = sanitize(title_column.text)
            output_data.append([title_text])  # Each title in its own row as the first cell

        # Extract Titles
        title_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        for parent in title_parents:
            children = parent.find_elements(By.XPATH, "./*")
            title_texts = [sanitize(child.text) for child in children if child.text.strip() != '']
            if title_texts:
                output_data.append(title_texts)

        # Extract Data
        data_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")
        for parent in data_parents:
            children = parent.find_elements(By.XPATH, "./*")
            child_texts = [sanitize(child.text) for child in children if child.text.strip() != '']
            if child_texts:
                output_data.append(child_texts)

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Read symbols from CSV file
symbols = []
csv_file_path = 'Symbols.csv'  # Update with your actual CSV file path
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            symbols.append(row[0])  # Assuming symbol is in the first column
except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")
    exit()

output_csv_file_path = 'OutputResults.csv'

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    for symbol in symbols:
        parent_child_data = process_url_dynamic(browser, symbol)
        for data_row in parent_child_data:
            # Prepend symbol to each row for clarity
            csv_writer.writerow([symbol] + data_row)
        print(f"Data written for symbol {symbol}")

browser.quit()
