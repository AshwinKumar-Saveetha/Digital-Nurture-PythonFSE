from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

from pages.base_page import BasePage


# Step 51

class SimpleFormPage(BasePage):

    MESSAGE_INPUT = (By.ID, "user-message")


    # Step 52

    SUBMIT_BUTTON = (
        By.XPATH,
        "//button[normalize-space()='Get Checked Value']"
    )

    DISPLAYED_MESSAGE = (By.ID, "message")

    def enter_message(self, text):
        message_input = self.wait_for_element(
            self.MESSAGE_INPUT
        )

        message_input.clear()
        message_input.send_keys(text)

    def click_submit(self):
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

        ActionChains(self.driver).move_to_element(
            submit_button
        ).click().perform()

    def get_displayed_message(self):
        displayed_message = WebDriverWait(
            self.driver,
            10
        ).until(
            EC.visibility_of_element_located(
                self.DISPLAYED_MESSAGE
            )
        )

        return displayed_message.text