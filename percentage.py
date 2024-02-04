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
    """Process each URL and extract specific data, including title columns and values."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # First, find and process the first three titleColumn-C9MdAMrq
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'titleColumn-C9MdAMrq')]")
        title_texts = [sanitize(title_column.text) for title_column in title_columns[:3]]  # Processing only the first 3

        # Then, find and process values-C9MdAMrq values-AtxjAQkN
        values_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")
        for index, values_parent in enumerate(values_parents):
            if index < len(title_texts):  # Ensure we don't exceed the titles list
                children = values_parent.find_elements(By.XPATH, "./*")
                child_texts = [sanitize(child.text) for child in children if child.text.strip() != '']
                output_data.append([title_texts[index]] + child_texts)

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Reading symbols from a predefined list for demonstration
symbols = ['4344', '2222']  # Example symbols

# Process each symbol and write to CSV
output_csv_file_path = 'OutputResults.csv'
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    for symbol in symbols:
        parent_child_data = process_url_dynamic(browser, symbol)
        for data_row in parent_child_data:
            csv_writer.writerow([symbol] + data_row)
        print(f"Data written for symbol {symbol}")

browser.quit()
