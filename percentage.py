from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    """Clean the text by removing non-printable characters."""
    return ''.join(char for char in text if char.isprintable())

def initialize_webdriver():
    """Initializes and returns a Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def process_url_dynamic(browser, symbol):
    """Extracts and organizes data from the webpage into a structured table format."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)
    structured_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Assuming you want to extract every piece of text from a specific class and separate them into individual cells
        elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        for element in elements:
            # Splitting the text into parts if necessary, or directly appending sanitized text
            text_parts = [sanitize(text) for text in element.text.split('\n')]  # Example of splitting by newline
            structured_data.append([symbol] + text_parts)
    
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return structured_data

def write_to_csv(output_csv_file_path, data_for_csv):
    """Writes the collected data into a CSV file."""
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        # Writing a header row (optional, customize as needed)
        csv_writer.writerow(["Symbol", "Data1", "Data2", "..."])  # Adjust column titles as per your data
        for row in data_for_csv:
            csv_writer.writerow(row)

def main():
    """Main function to orchestrate the web scraping and CSV writing."""
    browser = initialize_webdriver()
    symbols = ['4344', '2222']  # Define your symbols list here

    all_data_for_csv = []
    for symbol in symbols:
        symbol_data = process_url_dynamic(browser, symbol)
        all_data_for_csv.extend(symbol_data)  # Append data for each symbol to a single list

    # Write all extracted data into a single CSV file
    output_csv_file_path = 'OutputResults.csv'
    write_to_csv(output_csv_file_path, all_data_for_csv)
    print(f"All data written to {output_csv_file_path}")

    browser.quit()

if __name__ == "__main__":
    main()
