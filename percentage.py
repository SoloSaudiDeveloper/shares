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
    """Process each URL and extract specific data, including separated top row values and other values."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        # Wait for the dynamic content to load
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(@class, "financials")]'))
        )

        # Example XPath for top row (Years) - Adjust based on actual page structure
        top_row_xpath = '//*[contains(@class, "headerRow")]/div[contains(@class, "cell")]'
        top_row_elements = browser.find_elements(By.XPATH, top_row_xpath)
        top_row_texts = [sanitize(element.text) for element in top_row_elements if element.text.strip()]
        if top_row_texts:
            output_data.append(["Years"] + top_row_texts)  # Assuming the first row is years

        # Example XPaths for data rows - Adjust based on actual page structure
        data_row_xpath = '//*[contains(@class, "dataRow")]/div[contains(@class, "cell")]'
        data_rows = browser.find_elements(By.XPATH, data_row_xpath)
        for row in data_rows:
            row_texts = [sanitize(element.text) for element in row.find_elements(By.XPATH, './*') if element.text.strip()]
            if row_texts:
                output_data.append(row_texts)

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data


# Initialize Selenium WebDriver options for better performance and compatibility
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

def main():
    symbols = ['4344', '2222']
    output_csv_file_path = 'OutputResults.csv'

    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Include headers for better CSV structure
        csv_writer.writerow(["Symbol", "Data Type", "Year 1", "Year 2", "Year 3"])
        for symbol in symbols:
            symbol_data = process_url_dynamic(browser, symbol)
            for data_row in symbol_data:
                csv_writer.writerow([symbol] + data_row)
            print(f"Data written for symbol {symbol}")

    browser.quit()

if __name__ == "__main__":
    main()
