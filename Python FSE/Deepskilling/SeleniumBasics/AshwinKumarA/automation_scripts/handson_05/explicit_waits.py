from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

page_url = (
    "https://www.lambdatest.com/selenium-playground/"
    "bootstrap-alert-messages-demo"
)

# Step 36 - Explicit Wait

driver.get(page_url)

success_button = driver.find_element(
    By.XPATH,
    "//button[text()='Normal Success Message']"
)

success_button.click()

success_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//div[contains(@class,'alert-success') "
            "and contains(.,'Normal success message')]"
        )
    )
)

print("Step 36 - Alert text:")
print(success_alert.text)

assert "success" in success_alert.text.lower()

# Step 37 - Using time.sleep(3)

driver.get(page_url)

start_time = time.time()

driver.find_element(
    By.XPATH,
    "//button[text()='Normal Success Message']"
).click()

time.sleep(3)

sleep_alert = driver.find_element(
    By.XPATH,
    "//div[contains(@class,'alert-success') "
    "and contains(.,'Normal success message')]"
)

sleep_end_time = time.time()
sleep_duration = sleep_end_time - start_time

assert "success" in sleep_alert.text.lower()

print("\nStep 37 - Alert text using sleep:")
print(sleep_alert.text)
print(f"Time taken using sleep: {sleep_duration:.2f} seconds")

# Step 37 - Using Explicit Wait

driver.get(page_url)

start_time = time.time()

success_button = driver.find_element(
    By.XPATH,
    "//button[text()='Normal Success Message']"
)

success_button.click()

wait_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//div[contains(@class,'alert-success') "
            "and contains(.,'Normal success message')]"
        )
    )
)

wait_end_time = time.time()
wait_duration = wait_end_time - start_time

assert "success" in wait_alert.text.lower()

print("\nStep 37 - Alert text using explicit wait:")
print(wait_alert.text)
print(f"Time taken using explicit wait: {wait_duration:.2f} seconds")

# time.sleep() always waits for the full specified time.
# Explicit wait continues as soon as the required condition is satisfied.

# Step 38 - Wait Until the Button Is Clickable

driver.get(page_url)

# visibility_of_element_located waits until an element is visible in the DOM.
# element_to_be_clickable waits until an element is visible, enabled and ready to click.

clickable_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable(
        (By.XPATH, "//button[text()='Normal Success Message']")
    )
)

clickable_button.click()

clickable_alert = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located(
        (
            By.XPATH,
            "//div[contains(@class,'alert-success') "
            "and contains(.,'Normal success message')]"
        )
    )
)

print("\nStep 38 - Clickable button alert:")
print(clickable_alert.text)

# Step 39 - FluentWait

driver.get(
    "https://www.lambdatest.com/selenium-playground/"
    "table-pagination-demo"
)

fluent_wait = WebDriverWait(
    driver,
    10,
    poll_frequency=0.5,
    ignored_exceptions=(NoSuchElementException,)
)

table_row = fluent_wait.until(
    lambda current_driver: current_driver.find_element(
        By.XPATH,
        "//table[@id='table-id']/tbody/tr[1]"
    )
)

print("\nStep 39 - Dynamically loaded table row:")
print(table_row.text)

driver.quit()