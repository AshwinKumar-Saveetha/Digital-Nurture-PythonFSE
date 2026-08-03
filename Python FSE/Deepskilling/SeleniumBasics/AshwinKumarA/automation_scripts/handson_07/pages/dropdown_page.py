from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


# Step 54

class DropdownPage(BasePage):

    DAY_DROPDOWN = (By.ID, "select-demo")

    def select_day(self, day_name):
        dropdown_element = self.wait_for_element(
            self.DAY_DROPDOWN
        )

        day_dropdown = Select(dropdown_element)
        day_dropdown.select_by_visible_text(day_name)

        return day_dropdown.first_selected_option.text