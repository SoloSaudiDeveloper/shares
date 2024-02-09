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
    """Process each URL and extract specific data, including separated top row titles and other values."""
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    try:
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Extract and separately append each text from elements with the classes 'values-OWKkVLyj' and 'values-AtxjAQkN'
        top_row_elements = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-OWKkVLyj') and contains(@class, 'values-AtxjAQkN')]")
        top_row_texts = []
        for element in top_row_elements:
            if element.text.strip() != '':
                # Add each sanitized text as a separate entry to ensure they go into separate cells
                top_row_texts.extend([sanitize(text) for text in element.text.split('\n') if text.strip() != ''])

        # Add the collected top row texts as the first row for this symbol
        if top_row_texts:
            output_data.append(top_row_texts)

        # Proceed with extracting the other required data following the same logic as previously described
    
        # This includes handling titleColumn-C9MdAMrq and values-C9MdAMrq values-AtxjAQkN as per your specific requirements
     # Extract and process first three titleColumn-C9MdAMrq titles
        title_columns = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'titleColumn-C9MdAMrq')]")
        titles = [sanitize(title_column.text) for title_column in title_columns[:3]]  # Only first 3 titles

        # For each title, create a new row in output_data
        for title in titles:
            output_data.append([title])

        # Extract data for 'values-C9MdAMrq values-AtxjAQkN' and append to the corresponding title row
        data_parents = browser.find_elements(By.XPATH, f"{container_xpath}//*[contains(@class, 'values-C9MdAMrq') and contains(@class, 'values-AtxjAQkN')]")
        for index, parent in enumerate(data_parents[:3]):  # Assuming there is a direct match in count with titleColumn-C9MdAMrq
            children = parent.find_elements(By.XPATH, "./*")
            child_texts = [sanitize(child.text) for child in children if child.text.strip() != '']
            if child_texts:
                # Check to ensure there's a row to extend (offset by 1 due to top_row_texts)
                if len(output_data) > index + 1:
                    output_data[index + 1].extend(child_texts)

    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")

    return output_data



# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

symbols = ['4344', '2222']  # Example symbol list
output_csv_file_path = 'OutputResults.csv'

# Process each symbol and write to CSV
with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    for symbol in symbols:
        parent_child_data = process_url_dynamic(browser, symbol)
        for data_row in parent_child_data:
            csv_writer.writerow([symbol] + data_row)  # Prepend symbol to each row
        print(f"Data written for symbol {symbol}")

browser.quit()
