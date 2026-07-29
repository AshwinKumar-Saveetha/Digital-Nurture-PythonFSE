"""
Student Name: Ashwin Kumar A
Hands-On 4 - Task 2
"""

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


current_folder = Path(__file__).parent
screenshot_path = current_folder / "playground_screenshot.png"

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

try:
    driver.implicitly_wait(10)

    driver.get("https://www.lambdatest.com/selenium-playground/")

    print("Original window size:", driver.get_window_size())

    driver.set_window_size(1280, 800)

    # A fixed window size helps keep responsive page layouts consistent.
    print("New window size:", driver.get_window_size())

    driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

    assert "simple-form-demo" in driver.current_url
    print("URL assertion passed:", driver.current_url)

    driver.back()

    driver.execute_script(
        'window.open("https://www.google.com");'
    )

    print("Open tabs:", driver.window_handles)

    driver.switch_to.window(driver.window_handles[1])
    print("Google title:", driver.title)

    driver.switch_to.window(driver.window_handles[0])

    driver.save_screenshot(str(screenshot_path))
    print("Screenshot saved:", screenshot_path)

    input("Press Enter to close the browser...")

finally:
    driver.quit()
    print("Browser closed successfully.")