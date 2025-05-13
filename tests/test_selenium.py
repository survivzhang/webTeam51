from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    # Configure Chrome (remove headless if you want to see the browser)
    chrome_opts = Options()
    # chrome_opts.add_argument("--headless")  # uncomment to run headless
    service = Service()  # assumes chromedriver is on your PATH

    # Launch browser
    driver = webdriver.Chrome(service=service, options=chrome_opts)
    driver.get("http://localhost:5000")

    # Pause so you can see it—close with Ctrl+C or by closing the window
    input("Browser opened http://localhost:5000. Press ENTER to quit...")

    driver.quit()

if __name__ == "__main__":
    main()
