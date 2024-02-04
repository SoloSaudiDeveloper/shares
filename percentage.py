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

        # Extract title columns (first 3 only)
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'titleColumn-C9MdAMrq')]")
        for title_column in title_columns[:3]:  # Process only first 3
            title_text = sanitize(title_column.text)
            output_data.append([title_text])  # Each title in its own row, first cell

        # Extract Titles
        title_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        titles = [sanitize(child.text) for parent in title_parents for child in parent.find_elements(By.XPATH, "./*") if child.text.strip() != '']
        if titles:  # Only add if there's actual text extracted
            output_data.insert(0, titles)  # Insert titles at the beginning

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
csv_file_path = 'Symbols.csv'
symbols = []
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:  # Check if the row is not empty
                symbols.append(row[0])
    print("Symbols loaded.")
except FileNotFoundError as e:
    print(f"Error: File not found - {csv_file_path}")
    print(e)
    browser.quit()
    exit()
except IndexError as e:
    print("Error processing a row in the CSV file:", e)
    browser.quit()
    exit()

# Process each symbol and write to CSV
output_csv_file_path = 'OutputResults.csv'
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    for symbol in symbols:
        parent_child_data = process_url_dynamic(browser, symbol)
        for data_row in parent_child_data:
            csv_writer.writerow([symbol] + data_row)
        print(f"Data written for symbol {symbol}")

