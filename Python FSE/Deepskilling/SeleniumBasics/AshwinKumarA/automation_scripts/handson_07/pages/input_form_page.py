from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


# Step 57

class InputFormPage(BasePage):

    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.ID, "inputEmail4")
    PASSWORD_INPUT = (By.NAME, "password")
    COMPANY_INPUT = (By.NAME, "company")
    WEBSITE_INPUT = (By.NAME, "website")
    COUNTRY_DROPDOWN = (By.NAME, "country")
    CITY_INPUT = (By.NAME, "city")
    ADDRESS_ONE_INPUT = (By.NAME, "address_line1")
    ADDRESS_TWO_INPUT = (By.NAME, "address_line2")
    STATE_INPUT = (By.ID, "inputState")
    ZIP_CODE_INPUT = (By.NAME, "zip")

    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Submit']"
    )

    SUCCESS_MESSAGE = (
        By.XPATH,
        "//*[contains(text(), 'Thanks for contacting us')]"
    )

    def fill_form(self, name, email, phone, address):
        self.wait_for_element(
            self.NAME_INPUT
        ).send_keys(name)

        self.wait_for_element(
            self.EMAIL_INPUT
        ).send_keys(email)

        self.wait_for_element(
            self.PASSWORD_INPUT
        ).send_keys("Password123")

        self.wait_for_element(
            self.COMPANY_INPUT
        ).send_keys("Cognizant")

        self.wait_for_element(
            self.WEBSITE_INPUT
        ).send_keys("https://www.cognizant.com")

        country_element = self.wait_for_element(
            self.COUNTRY_DROPDOWN
        )

        country_dropdown = Select(country_element)
        country_dropdown.select_by_visible_text("India")

        self.wait_for_element(
            self.CITY_INPUT
        ).send_keys("Chennai")

        self.wait_for_element(
            self.ADDRESS_ONE_INPUT
        ).send_keys(address)

        self.wait_for_element(
            self.ADDRESS_TWO_INPUT
        ).send_keys("Tamil Nadu")

        self.wait_for_element(
            self.STATE_INPUT
        ).send_keys("Tamil Nadu")

        # The present form has no phone field.
        # The phone argument is used as the numeric Zip Code value.
        self.wait_for_element(
            self.ZIP_CODE_INPUT
        ).send_keys(phone)

    def submit_form(self):
        submit_button = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.element_to_be_clickable(
                self.SUBMIT_BUTTON
            )
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            submit_button
        )

        submit_button.click()

    def get_success_message(self):
        success_message = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                self.SUCCESS_MESSAGE
            )
        )

        return success_message.text