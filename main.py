import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

def process_element(element_html):
    soup = BeautifulSoup(element_html, 'html.parser')
    return soup.get_text()

def process_url(browser, url, xpath_template):
    print(f"Processing URL: {url}")
    browser.get(url)

    output_data = []
    index = 1

    while True:
        current_xpath = xpath_template.format(index)
        try:
            element = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, current_xpath)))
            element_html = element.get_attribute('outerHTML')
            output_data.append(process_element(element_html))
            index += 1
        except Exception as e:
            print(f"No more data found for URL at index {index}.")
            break

    return output_data

def main(csv_file_path, output_csv_file_path):
    # Initialize Selenium WebDriver options
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--disable-gpu")

    # Initialize Selenium WebDriver
    browser = webdriver.Chrome(options=chrome_options)

    data_to_process = []

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)  # Skip the header
            data_to_process = [row for row in csv_reader]
    except FileNotFoundError:
        print(f"Error: File not found - {csv_file_path}")
        return

    if not data_to_process:
        print("No data to process.")
    else:
        with open(output_csv_file_path, 'w', newline='', encoding='utf-8') as out_csvfile:
            csv_writer = csv.writer(out_csvfile)
            for row in data_to_process:
                url, xpath_template = row[0], row[1]
                print(f"Processing: {url}")
                data = process_url(browser, url, xpath_template)
                for element_text in data:
                    csv_writer.writerow([url, element_text])

    browser.quit()

# Replace with your actual file paths
csv_file_path = 'xpath.csv'
output_csv_file_path = 'OutputResults.csv'
main(csv_file_path, output_csv_file_path)
