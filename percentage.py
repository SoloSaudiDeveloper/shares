import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Function to process each URL with provided XPaths
def process_url_dynamic(browser, symbol, xpaths_list):
    print(f"Processing symbol {symbol}...")
    url = f"https://www.tradingview.com/symbols/TADAWUL-{symbol}/financials-dividends/"
    browser.get(url)

    output_data = []

    # Wait for the page to load using the first XPath as an indicator
    WebDriverWait(browser, 20).until(EC.presence_of_element_located((By.XPATH, xpaths_list[0][0])))

    # Process each row of XPaths
    for xpaths in xpaths_list:
        row_data = []
        for xpath in xpaths:
            try:
                element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                row_data.append(element.text)
            except TimeoutException:
                print(f"Timed out waiting for element with XPath: {xpath}.")
                row_data.append('N/A')  # Use 'N/A' for missing data
        output_data.extend(row_data)  # Add the row data to output_data

    # Split the output_data into chunks of 7 columns
    return [output_data[i:i+7] for i in range(0, len(output_data), 7)]

# Initialize Selenium WebDriver options
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument("--disable-gpu")

# Initialize Selenium WebDriver
browser = webdriver.Chrome(options=chrome_options)

# Read symbols from the CSV file
csv_file_path = 'Symbols.csv'  # Update with your actual path to the CSV file
output_csv_file_path = 'percentage.csv'  # Update with your desired output file path

symbols = []
try:
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        symbols = [row[0] for row in csv_reader if row]  # Read symbols, skip empty rows
    print("Symbols loaded.")
except FileNotFoundError:
    print(f"Error: File not found - {csv_file_path}")
    browser.quit()
    exit()

# Hardcoded XPaths for each symbol, grouped by the layout row
xpaths_list = [
    # XPaths for all rows
       [
        '//*[@id="js-category-content"]/div[1]/div[1]/div/div/div/h2',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[3]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[4]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[5]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[6]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[1]/div[4]/div[7]',


        # ... other XPaths for row 1
    ],
    # Second row XPaths
    [
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]/div[3]/div[2]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]/div[5]/div[3]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]/div[5]/div[4]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]/div[5]/div[5]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]/div[5]/div[6]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[2]/div[5]/div[7]',
        # ... other XPaths for the second row
    ],
    # Third row XPaths
    [
        
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]/div[3]/div[2]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]/div[5]/div[3]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]/div[5]/div[4]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]/div[5]/div[5]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]/div[5]/div[6]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[3]/div[5]/div[7]',
        
  
        
        # ... other XPaths for the third row
    ],
    # Fourth row XPaths
    [
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]/div[3]/div[2]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]/div[5]/div[3]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]/div[5]/div[4]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]/div[5]/div[5]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]/div[5]/div[6]',
        '//*[@id="js-category-content"]/div[2]/div/div/div[5]/div[2]/div/div[1]/div[4]/div[5]/div[7]',

      
        
        # ... other XPaths for the fourth row
    ],
    # ... Add other XPaths here
]

# Check if symbols were loaded
if not symbols:
    print("No symbols to process.")
    browser.quit()
else:
    # Open the output CSV file for writing
    with open(output_csv_file_path, 'w', newline='', encoding='utf-8-sig') as out_csvfile:
        csv_writer = csv.writer(out_csvfile)
        
        # Write header row for 7 columns
        header = ['Symbol', 'Data1', 'Data2', 'Data3', 'Data4', 'Data5', 'Data6', 'Data7']
        csv_writer.writerow(header)
        
        # Process each symbol
        for symbol in symbols:
            # Write the symbol and the data in groups of 7 columns
            data_chunks = process_url_dynamic(browser, symbol, xpaths_list)
            for chunk in data_chunks:
                csv_writer.writerow([symbol] + chunk)
            print(f"Data written for symbol {symbol}")

# Close the browser after all symbols have been processed
browser.quit()
