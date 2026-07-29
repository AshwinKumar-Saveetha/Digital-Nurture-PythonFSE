"""
Student Name: Ashwin Kumar A
Hands-On 4 - Task 1

WebDriver:
WebDriver controls the browser using Python commands through ChromeDriver.

Selenium Grid:
Selenium Grid runs tests on multiple browsers or computers in parallel.

Selenium IDE:
Selenium IDE records and plays back browser actions and can generate code.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

try:
    driver.implicitly_wait(10)

    # Implicit wait applies to element searches globally.
    # Explicit waits are preferred because they wait for a specific condition.

    driver.get("https://www.lambdatest.com/selenium-playground/")

    print("Page title:", driver.title)
    print("Headless execution completed successfully.")

finally:
    driver.quit()
    print("Browser closed successfully.")