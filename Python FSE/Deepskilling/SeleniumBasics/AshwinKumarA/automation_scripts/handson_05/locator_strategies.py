from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

driver.get("https://www.lambdatest.com/selenium-playground/")

driver.find_element(By.LINK_TEXT, "Simple Form Demo").click()

# Step 32 - Locator Strategies

driver.find_element(By.ID, "user-message")

driver.find_element(By.CLASS_NAME, "border")

driver.find_element(By.TAG_NAME, "input")

driver.find_element(
    By.XPATH,
    "/html/body/div[1]/div/main/div/section[2]/div/div/div/div[1]/div[2]/div/div[1]/input"
)

driver.find_element(
    By.XPATH,
    "//input[@id='user-message']"
)

# Step 33 - CSS Selectors

driver.find_element(
    By.CSS_SELECTOR,
    "#user-message"
)

driver.find_element(
    By.CSS_SELECTOR,
    "input[placeholder='Please enter your Message']"
)

driver.find_element(
    By.CSS_SELECTOR,
    "div > input#user-message"
)

# Step 34 - XPath text() and contains()

driver.back()

driver.find_element(By.LINK_TEXT, "Checkbox Demo").click()

driver.find_element(
    By.XPATH,
    "//label[text()='Option 1']"
)

driver.find_elements(
    By.XPATH,
    "//label[contains(text(),'Option')]"
)

# Step 35 - Locator Ranking

# 1. ID - Unique and easy to read
# 2. Name - Readable but may not always be unique
# 3. CSS Selector - Fast and flexible
# 4. Class Name - A class may be shared by many elements
# 5. Tag Name - Usually matches many elements
# 6. XPath - Relative XPath is better than Absolute XPath

driver.quit()