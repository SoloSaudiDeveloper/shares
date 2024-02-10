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
    """Process each URL and extract specific data, placing it in the specified order in the output."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []  # Initialize to hold all rows for this symbol

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Extract texts from 'values-OWKkVLyj values-AtxjAQkN' for the top row
        top_row_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        top_row_texts = [sanitize(element.text) for element in top_row_elements for text in element.text.split('\n') if text.strip() != '']

        # If there are texts for the top row, create the first row for this symbol
        if top_row_texts:
            output_data.append([symbol] + top_row_texts)

        # Extract and combine the first three 'titleColumn-C9MdAMrq' and their corresponding 'values-C9MdAMrq values-AtxjAQkN'
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'titleColumn-C9MdAMrq')]")
        values_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")

        combined_data = []
        for index in range(min(3, len(title_columns), len(values_parents))):  # Process up to first 3 matches
            title_text = sanitize(title_columns[index].text)
            children_texts = [sanitize(child.text) for child in values_parents[index].find_elements(By.XPATH, "./*") if child.text.strip() != '']
            combined_data.extend([title_text] + children_texts)  # Combine title and values in one list

        # Add combined data as a new row following the top row
        if combined_data:
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
                csv_writer.writerow(data_row)  # Data rows already start with symbol
            print(f"Data written for symbol {symbol}")

    browser.quit()

if __name__ == "__main__":
    main()
