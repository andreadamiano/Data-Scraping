from selenium import webdriver
from selenium.webdriver.chrome.options import Options

# Configure Chrome to run in headless mode (no GUI)
options = Options()
options.add_argument("--headless")  # Remove this line to see the browser
options.add_argument("--disable-notifications")

# Initialize the WebDriver (Chrome)
driver = webdriver.Chrome(options=options)

try:
    # Load a dynamic page (e.g., Facebook profile)
    url = "https://pythonscraping.com/pages/javascript/ajaxDemo.html"
    driver.get(url)
    
    # Wait for JavaScript to load (optional, but recommended)
    driver.implicitly_wait(5)  # Waits up to 5 sec for elements to appear
    
    # Get the fully rendered HTML
    html = driver.page_source
    print(html)  # Now contains JS-generated content!
    
finally:
    driver.quit()  # Close the browser