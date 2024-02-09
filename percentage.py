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
    """Process each URL and extract specific data, including separated top row values."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Extract every text from elements with the class 'values-OWKkVLyj values-AtxjAQkN' and separate them
        top_row_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        # Flatten all texts into a single list, each text becomes a separate entry
        top_row_texts = [sanitize(text) for element in top_row_elements for text in element.text.split('\n') if text.strip() != '']
        if top_row_texts:
            output_data.append(top_row_texts)  # Append as the top row without a title

        # Continue with other data extraction as before, adapted to your specific needs...

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data

def initialize_webdriver():
    """Initializes and returns a Selenium WebDriver with specified options."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def write_to_csv(output_csv_file_path, data_for_csv):
    """Writes provided data to a CSV file at the specified path."""
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in data_for_csv:
            csv_writer.writerow(row)

def main():
    """Main function to orchestrate the web scraping and CSV writing process."""
    browser = initialize_webdriver()
    symbols = ['4344', '2222']  # Define your symbols list here
    all_data_for_csv = []

    for symbol in symbols:
        symbol_data = process_url_dynamic(browser, symbol)
        # Prefix each row with the symbol for clarity
        for data_row in symbol_data:
            all_data_for_csv.append([symbol] + data_row)

    # Specify the output CSV file path
    output_csv_file_path = 'OutputResults.csv'
    # Write all collected data to the CSV
    write_to_csv(output_csv_file_path, all_data_for_csv)
    print(f"All data written to {output_csv_file_path}")

    browser.quit()

if __name__ == "__main__":
    main()
