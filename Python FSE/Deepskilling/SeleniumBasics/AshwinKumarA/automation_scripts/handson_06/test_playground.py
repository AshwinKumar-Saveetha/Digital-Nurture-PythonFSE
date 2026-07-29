# Step 40

import pytest

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

# Step 42
# Step 45

@pytest.mark.parametrize(
    "message",
    ["Hello", "Selenium Automation", "12345"]
)
def test_simple_form_submission(driver, base_url, message):
    driver.get(base_url + "simple-form-demo")

    message_input = driver.find_element(
        By.ID,
        "user-message"
    )

    message_input.send_keys(message)

    driver.find_element(
        By.ID,
        "showInput"
    ).click()

    displayed_message = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.ID, "message")
        )
    )

    assert displayed_message.text == message   # "Wrong Message"


# Step 43

def test_checkbox_interaction(driver, base_url):
    driver.get(base_url + "checkbox-demo")

    first_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "(//input[@type='checkbox' and not(@disabled)])[1]"
            )
        )
    )

    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});",
        first_checkbox
    )

    if not first_checkbox.is_selected():
        driver.execute_script(
            "arguments[0].click();",
            first_checkbox
        )

    assert first_checkbox.is_selected()

    driver.execute_script(
        "arguments[0].click();",
        first_checkbox
    )

    assert not first_checkbox.is_selected()

# Step 49

def test_dropdown_selection(driver, base_url):
    driver.get(base_url + "select-dropdown-demo")

    dropdown = Select(
        driver.find_element(
            By.ID,
            "select-demo"
        )
    )

    dropdown.select_by_visible_text("Wednesday")

    selected_option = dropdown.first_selected_option

    assert selected_option.text == "Wednesday"