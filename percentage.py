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
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)
    structured_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Assuming 'values-OWKkVLyj values-AtxjAQkN' contains the headers
        headers_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        headers = [sanitize(element.text) for element in headers_elements if element.text.strip() != '']
        
        # Ensure headers are in the first row if not already included
        if structured_data == []:
            structured_data.append(headers)
        
        # Now, extract and structure data for each 'data-point' class (or similar)
        # Example: Extracting data points
        data_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'data-point-class')]")
        data_row = [symbol]  # Start the row with the symbol
        for element in data_elements:
            data = sanitize(element.text)
            data_row.append(data)  # Each data point added as a separate cell
        
        structured_data.append(data_row)
    
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
    symbols = ['4344', '2222']  # Example symbols list

    all_data_for_csv = []
    for symbol in symbols:
        symbol_data = process_url_dynamic(browser, symbol)
        all_data_for_csv.extend(symbol_data)  # Collecting data for all symbols

    output_csv_file_path = 'OutputResults.csv'
    write_to_csv(output_csv_file_path, all_data_for_csv)
    print("All data written to", output_csv_file_path)

    browser.quit()


if __name__ == "__main__":
    main()
