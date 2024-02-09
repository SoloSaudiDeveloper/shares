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
    """Extract and organize data from the webpage into a structured table format."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    structured_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Top row titles
        top_row_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        top_row = [sanitize(element.text) for element in top_row_elements if element.text.strip() != '']
        structured_data.append(top_row)  # This will be the table header

        # Following rows: Example for extracting additional data
        # Implement logic to extract other required data and append to structured_data

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return structured_data

def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def write_to_csv(output_csv_file_path, data_for_csv):
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in data_for_csv:
            csv_writer.writerow(row)

def main():
    browser = initialize_webdriver()
    symbols = ['4344', '2222']  # Example symbols

    for symbol in symbols:
        data_for_csv = process_url_dynamic(browser, symbol)
        output_csv_file_path = f'OutputResults_{symbol}.csv'
        write_to_csv(output_csv_file_path, data_for_csv)
        print(f"Data written to {output_csv_file_path} for symbol {symbol}")

    browser.quit()

if __name__ == "__main__":
    main()
