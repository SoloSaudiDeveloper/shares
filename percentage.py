import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Selenium WebDriver
def initialize_webdriver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

# Function to sanitize text
def sanitize(text):
    return ''.join(char for char in text if char.isprintable())

# Function to process each URL with provided symbol
def process_url_dynamic(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    try:
        # Wait for the page container to load
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Your specific data extraction logic here

        # Example: Extract titles
        titles_xpath = f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]"
        titles = [sanitize(elm.text) for elm in browser.find_elements(By.XPATH, titles_xpath)]

        # Example: Extract data rows
        data_xpath = f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]"
        data_rows = [[sanitize(elm.text) for elm in row.find_elements(By.XPATH, "./*")] for row in browser.find_elements(By.XPATH, data_xpath)]

        # Combine titles and data
        output_data = titles + [item for sublist in data_rows for item in sublist]

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")
        output_data = []

    return output_data

# Main function to run the script
def main(symbols_csv_file_path, output_csv_file_path):
    browser = initialize_webdriver()
    symbols = ['4344', '2222']  # Directly using symbols for demonstration

    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)

        for symbol in symbols:
            data_row = process_url_dynamic(browser, symbol)
            csv_writer.writerow([symbol] + data_row)
            print(f"Data written for symbol {symbol}")

    browser.quit()

if __name__ == "__main__":
    symbols_csv_file_path = 'Symbols.csv'  # Ensure this file exists in your directory
    output_csv_file_path = 'OutputResults.csv'
    main(symbols_csv_file_path, output_csv_file_path)
