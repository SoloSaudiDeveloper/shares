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
    """Process each URL and extract specific data, focusing on desired elements."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Find top row elements excluding elements with 'alignLeft-OxVAcLqi'
        top_row_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        for element in top_row_elements:
            # Process only children with 'container-OxVAcLqi' excluding those also with 'alignLeft-OxVAcLqi'
            child_elements = element.find_elements(By.XPATH, "./*[contains(@class, 'container-OxVAcLqi') and not(contains(@class, 'alignLeft-OxVAcLqi'))]")
            child_texts = [sanitize(child.text) for child in child_elements if child.text.strip() != '']
            if child_texts:
                output_data.append(child_texts)

        # Extract first three titleColumn-C9MdAMrq and their corresponding values excluding 'alignLeft-OxVAcLqi'
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'titleColumn-C9MdAMrq')]")
        values_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")

        for index in range(min(3, len(title_columns), len(values_parents))):
            title_text = sanitize(title_columns[index].text)
            # Filter for specific child class patterns
            child_elements = values_parents[index].find_elements(By.XPATH, "./*[contains(@class, 'container-OxVAcLqi') and not(contains(@class, 'alignLeft-OxVAcLqi'))]")
            children_texts = [sanitize(child.text) for child in child_elements if child.text.strip() != '']
            if children_texts:
                output_data.append([title_text] + children_texts)

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
        header = ['Symbol', 'Info'] + ['Data ' + str(i) for i in range(1, 6)]  # Adjust according to your data needs
        csv_writer.writerow(header)
        for symbol in symbols:
            symbol_data = process_url_dynamic(browser, symbol)
            for data_row in symbol_data:
                row = [symbol] + data_row
                csv_writer.writerow(row)  # Write the modified row structure
            print(f"Data written for symbol {symbol}")

    browser.quit()

if __name__ == "__main__":
    main()
