# Step 40

import pytest

from pages.simple_form_page import SimpleFormPage
from pages.checkbox_page import CheckboxPage
from pages.dropdown_page import DropdownPage
from pages.input_form_page import InputFormPage


# Step 42
# Step 45
# Step 55

@pytest.mark.parametrize(
    "message",
    ["Hello", "Selenium Automation", "12345"]
)
def test_simple_form_submission(driver, base_url, message):
    page = SimpleFormPage(driver)

    page.navigate_to(base_url + "simple-form-demo")
    page.enter_message(message)
    page.click_submit()

    assert page.get_displayed_message() == message


# Step 43
# Step 56

def test_checkbox_interaction(driver, base_url):
    page = CheckboxPage(driver)

    page.navigate_to(base_url + "checkbox-demo")

    page.check_option(0)
    assert page.is_option_checked(0)

    page.uncheck_option(0)
    assert not page.is_option_checked(0)


# Step 49
# Step 56

def test_dropdown_selection(driver, base_url):
    page = DropdownPage(driver)

    page.navigate_to(base_url + "select-dropdown-demo")

    selected_day = page.select_day("Wednesday")

    assert selected_day == "Wednesday"


# Step 57

def test_input_form_submit(driver, base_url):
    page = InputFormPage(driver)

    page.navigate_to(base_url + "input-form-demo")

    page.fill_form(
        name="Ashwin Kumar",
        email="ashwin@example.com",
        phone="600056",
        address="Chennai"
    )

    page.submit_form()

    assert (
        page.get_success_message()
        == "Thanks for contacting us, we will get back to you shortly."
    )


# Step 59
#
# In a flat Selenium script, if the Submit button ID changes from
# "submit" to "btn-submit", the locator must be updated in every test
# where that button is directly located.
#
# In the Page Object Model, the Submit button locator is stored in one
# page class. Therefore, the locator needs to be updated only once in
# that page class, and all tests using its page method continue to work.