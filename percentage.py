from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def sanitize(text):
    return ''.join(char for char in text if char.isprintable())

def process_url_dynamic(browser, symbol):
    print(f"Processing symbol {symbol}...")
    url = f"https://ar.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    try:
        # Wait for the page container to load to ensure the page has loaded
        container_xpath = '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]'
        WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, container_xpath)))

        # Directly find elements with the class `container-OxVAcLqi`
        container_elements = browser.find_elements(By.XPATH, f"{container_xpath}//div[contains(@class, 'container-OxVAcLqi')]")

        # Concatenate text from all matching elements
        concatenated_text = ' | '.join([sanitize(element.text) for element in container_elements])

        return concatenated_text
    except Exception as e:
        print(f"An error occurred while processing {symbol}: {e}")
        return ""

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
browser = webdriver.Chrome(options=chrome_options)

# Placeholder for your symbols list loading mechanism
symbols = ['SYMBOL1', 'SYMBOL2']  # Example symbol list, replace with actual loading mechanism
output_csv_file_path = 'OutputResults.csv'  # Change as needed

with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(['Symbol', 'Data'])  # Writing header row

    for symbol in symbols:
        concatenated_data = process_url_dynamic(browser, symbol)
        if concatenated_data:  # Only write if there's data
            csv_writer.writerow([symbol, concatenated_data])
            print(f"Data written for symbol {symbol}")
        else:
            print(f"No data found for symbol {symbol}")

browser.quit()
