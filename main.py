from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def google_search(query):
    options = Options()
    options.headless = True
    options.add_argument("--no-sandbox")  # This make Chrome run as root in Docker
    options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
    options.add_argument("--disable-gpu")  # applicable to windows os only
    options.add_argument("--start-maximized")
    options.add_argument("--remote-debugging-port=9222")

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
