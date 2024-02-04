from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    """Clean the text by removing non-printable characters."""
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol, csv_writer):
    """Process each URL and extract data from specified classes, organizing by parent-child relationships."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Titles
        titles = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj values-AtxjAQkN')]")
        title_texts = [sanitize(title.text) for title in titles]
        csv_writer.writerow([symbol, 'Titles'] + title_texts)

        # Parents and children
        parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq values-AtxjAQkN')]")
        for parent in parents:
            # Extract text from the parent element itself, if necessary
            # parent_text = sanitize(parent.text)
            # csv_writer.writerow([symbol, 'Parent', parent_text])
            
            children = parent.find_elements(By.XPATH, ".//*[contains(@class, 'child-class-here')]")  # Update your child class
            child_texts = [sanitize(child.text) for child in children]
            # For each parent, write a new row for its children
            for child_text in child_texts:
                csv_writer.writerow([symbol, 'Child', child_text])

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

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
    # There's no single header row because of the variable structure

    for symbol in symbols:
        process_url_dynamic(browser, symbol, csv_writer)

browser.quit()
