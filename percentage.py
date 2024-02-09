import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def sanitize(text):
    """Clean the text by removing non-printable characters."""
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    """Extract and organize data from the webpage into a structured table format for a given symbol."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)
    
    structured_data = []
    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))
        
        # Extract titles (values-OWKkVLyj values-AtxjAQkN)
        title_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        titles = [sanitize(elm.text) for elm in title_elements if elm.text.strip() != '']
        structured_data.append(["Symbol"] + titles)  # First row with titles
        
        # Extract special titles (titleColumn-C9MdAMrq), first 3 occurrences
        special_title_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'titleColumn-C9MdAMrq')]")
        special_titles = [sanitize(elm.text) for elm in special_title_elements[:3] if elm.text.strip() != '']  # First 3 special titles
        
        # Extract data (values-C9MdAMrq values-AtxjAQkN) and match with special titles
        for title in special_titles:
            data_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")
            data_row = [sanitize(elm.text) for elm in data_elements if elm.text.strip() != '']
            structured_data.append([symbol] + data_row)  # Append symbol and extracted data
        
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return structured_data

def initialize_webdriver():
    """Initialize and return a Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    return webdriver.Chrome(options=chrome_options)

def write_to_csv(output_csv_file_path, data_for_csv):
    """Write provided data to a CSV file."""
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in data_for_csv:
            csv_writer.writerow(row)

def main():
    """Main function to orchestrate the web scraping and data writing process."""
    browser = initialize_webdriver()
    symbols = ['4344', '2222']  # Example symbols

    all_data_for_csv = []
    for symbol in symbols:
        symbol_data = process_url_dynamic(browser, symbol)
        all_data_for_csv.extend(symbol_data)  # Aggregate data for all symbols
    
    # Write aggregated data to a single CSV file
    output_csv_file_path = 'OutputResults.csv'
    write_to_csv(output_csv_file_path, all_data_for_csv)
    print(f"All data written to {output_csv_file_path}")

    browser.quit()

if __name__ == "__main__":
    main()
