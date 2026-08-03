from selenium.webdriver.common.by import By

from pages.base_page import BasePage


# Step 53

class CheckboxPage(BasePage):

    CHECKBOXES = (By.CSS_SELECTOR, "input[type='checkbox']")

    def check_option(self, index):
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)

        if not checkboxes[index].is_selected():
            checkboxes[index].click()

    def uncheck_option(self, index):
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)

        if checkboxes[index].is_selected():
            checkboxes[index].click()

    def is_option_checked(self, index):
        checkboxes = self.driver.find_elements(*self.CHECKBOXES)
        return checkboxes[index].is_selected()