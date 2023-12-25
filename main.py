from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

def google_search(query):
    # Set up headless option
    options = Options()
    options.headless = True

    # Set path to chromedriver as per your configuration
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to Google
        driver.get("https://www.google.com")

        # Find the search box
        search_box = driver.find_element_by_name("q")

        # Type in the search query
        search_box.send_keys(query)

        # Hit Enter to search
        search_box.send_keys(Keys.RETURN)

        # Wait for the results to load
        driver.implicitly_wait(5)

        # Find and print the titles of search results
        titles = driver.find_elements_by_tag_name("h3")
        for title in titles:
            print(title.text)

    finally:
        # Close the browser
        driver.quit()

# Replace 'OpenAI' with your search query
google_search("OpenAI")
