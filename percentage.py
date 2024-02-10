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
    """Process each URL and extract specific data, organizing it according to new requirements."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []  # Initialize list to hold all rows of data for this symbol

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Extract texts for the top row from 'values-OWKkVLyj values-AtxjAQkN'
        top_row_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        top_row_texts = [sanitize(text) for element in top_row_elements for text in element.text.split('\n') if text.strip() != '']
        if top_row_texts:
            output_data.append([symbol] + top_row_texts)  # Top row with symbol and texts in separate cells

        # For subsequent data, start directly with values without additional titles in the second cell
        combined_data = []
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'titleColumn-C9MdAMrq')]")
        values_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")

        for index in range(min(len(title_columns), len(values_parents))):
            title_text = sanitize(title_columns[index].text)  # Though not directly used, could be useful for debugging
            child_texts = [sanitize(child.text) for child in values_parents[index].find_elements(By.XPATH, "./*") if child.text.strip() != '']
            combined_data.extend(child_texts)  # Aggregate data from the first three 'values-' elements

        # Append the combined data as a single row, if there's any, after the top row
        if combined_data:
            # Ensure there's a row for the symbol and insert combined data into the second position
            if len(output_data) >= 1:
                output_data.append([symbol] + combined_data)
            else:  # If, for some reason, the top row wasn't added
                output_data.append([symbol] + combined_data)

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

def main():
    symbols = ['4344', '2222']  # Define your symbols list here
    output_csv_file_path = 'OutputResults.csv'

    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
        csv_writer = csv.writer(csvfile)
        for symbol in symbols:
            symbol_data = process_url_dynamic(browser, symbol)
            for data_row in symbol_data:
                csv_writer.writerow(data_row)  # Each row already starts with the symbol
            print(f"Data written for symbol {symbol}")

    browser.quit()

if __name__ == "__main__":
    main()
