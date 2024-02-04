from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def process_symbol(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)
    
    # Wait for the container to ensure the page has loaded
    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="js-category-content"]')))
    
    # Extract titles
    titles_elements = browser.find_elements(By.XPATH, "//*[contains(@class, 'values-OWKkVLyj values-AtxjAQkN')]/*")
    titles = [title.text for title in titles_elements if title.text != '']
    
    # Assuming extraction of first 3 titles for structure, adjust as necessary
    titles = titles[:3] if len(titles) > 3 else titles
    
    # Extract values under each title
    values = []
    for i, title in enumerate(titles, start=1):
        # Adjust the XPATH to correctly target the children under each title
        value_elements = browser.find_elements(By.XPATH, f"//*[contains(@class, 'values-C9MdAMrq values-AtxjAQkN')][{i}]/*")
        values.extend([value.text for value in value_elements])
    
    return [symbol] + titles + values

def read_symbols_from_csv(csv_file_path):
    symbols = []
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if row:  # Skip empty rows
                symbols.append(row[0])
    return symbols

def main():
    symbols_csv_file_path = 'Symbols.csv'  # Ensure this matches your file's name
    output_csv_file_path = 'OutputResults.csv'
    
    browser = initialize_webdriver()
    symbols = read_symbols_from_csv(symbols_csv_file_path)
    
    with open(output_csv_file_path, mode='w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        for symbol in symbols:
            row_data = process_symbol(browser, symbol)
            csv_writer.writerow(row_data)
            print(f"Data written for symbol {symbol}")
    
    browser.quit()

if __name__ == "__main__":
    main()
