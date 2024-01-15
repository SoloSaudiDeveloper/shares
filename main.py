import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def process_url(browser, url, xpath_template):
    print(f"Processing URL: {url}")
    browser.get(url)

    output_data = []
    index = 1  # Start the index at 1

    while True:
        # Replace the index placeholder with the current index
        current_xpath = xpath_template.format(index)
        try:
            # Wait for the element and get its HTML
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, current_xpath)))
            element_html = element.get_attribute('outerHTML')
            output_data.append(process_element(element_html))
            index += 1
        except Exception as e:
            print(f"No more data found for URL at index {index}.")
            break

    return output_data

def process_element(element_html):
    soup = BeautifulSoup(element_html, 'html.parser')
    element_text = soup.get_text()
    # Here you could process the text further if needed
    return element_text

#Path to the input CSV file
csv_file_path = 'YourInputCsvFileName.csv' # Replace with your actual input file name

#Path to the output CSV file
output_csv_file_path = 'OutputResults.csv'

# Initialize Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")

# Initialize Selenium WebDriver
browser = webdriver.Chrome(options=chrome_options)

# Path to the input CSV file
csv_file_path = 'xpath.csv'  # Replace with your actual input file name

# Path to the output CSV file
output_csv_file_path = 'OutputResults.csv'

# Read data from the CSV file
print("Reading data from the CSV file...")
data_to_process = []
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)  # Skip the header if there is one
        data_to_process = [row for row in csv_reader]
    print(f"Data loaded: {len(data_to_process)} records")
except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")
    # Check if data is available to process
if not data_to_process:
    print("No data to process.")
    browser.quit()  # Exit if no data to process
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        # Process each row from the input CSV
        for row in data_to_process:
            url = row[0]  # The website URL is in the first column
            xpath_template = row[1]  # The XPath template is in the second column
            print(f"Processing: {url}")
            data = process_url(browser, url, xpath_template)
            if data:
                for element_text in data:
                    print(f"Writing to CSV: {element_text}")
                    csv_writer.writerow([url, element_text])
            else:
                print(f"No data found for URL: {url}")

# Don't forget to close the browser after all URLs have been processed
browser.quit()
