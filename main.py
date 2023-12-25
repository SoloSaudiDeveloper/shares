import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def process_url(number, browser):
    print(f"Processing symbol {number}...")
    url = f"https://www.tradingview.com/symbols/TADAWUL-{number}/financials-dividends/"
    browser.get(url)

    primary_xpath_base = "//*[@id='js-category-content']/div[2]/div/div/div[8]/div[2]/div/div[1]/div[{}]"
    secondary_xpath = "//*[@id='js-category-content']/div[2]/div/div/div[3]/div/strong"
    div_index = 1
    output_data = []

    try:
        WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, primary_xpath_base.format(1))))
        while True:
            primary_element_xpath = primary_xpath_base.format(div_index)
            try:
                element_html = browser.find_element(
                    By.XPATH, primary_element_xpath).get_attribute('outerHTML')
                process_element(element_html, number, output_data)
                div_index += 1
            except Exception:
                break
    except Exception as e:
        try:
            element_html = browser.find_element(
                By.XPATH, secondary_xpath).get_attribute('outerHTML')
            process_element(element_html, number, output_data)
        except Exception:
            pass

    return output_data

def process_element(element_html, number, output_data):
    soup = BeautifulSoup(element_html, 'html.parser')
    element_text = soup.get_text()
    pattern = r'(\d{1,2}/\d{1,2}/\d{4})|(\d+\.\d+)|(\w+)'
    matches = re.findall(pattern, element_text)
    flattened_matches = [item for sublist in matches for item in sublist if item]
    separated_text = ' '.join(flattened_matches)
    output_data.append(f"{number}: {separated_text}")

# Initialize Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")
browser = webdriver.Chrome(options=chrome_options)

# Path to the CSV file
csv_file_path = 'Symbols.csv'

# Read symbols from the CSV file
symbols = []
with open(csv_file_path, newline='') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader, None)  # Skip the header if there is one
    symbols = [row[0] for row in csv_reader]

# Process each symbol and print the result
for number in symbols:
    data = process_url(number, browser)
    for item in data:
        print(item)

browser.quit()
