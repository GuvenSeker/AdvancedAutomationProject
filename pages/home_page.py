from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec

from pages.base_page import BasePage


class HomePage(BasePage):
    CATEGORY_COMPANY = (By.XPATH, "//a[contains(text(), 'Company')]")
    CATEGORY_CAREERS = (By.LINK_TEXT, 'Careers')
    website_url = 'https://useinsider.com/'

    def check(self):
        self.wait.until(ec.visibility_of_element_located(self.CATEGORY_COMPANY), 'No company button on the page')

    def hover_company_from_navigation_bar(self):
        """
        Hovers to 'Company' element on navigation bar

        """
        self.hover_element(*self.CATEGORY_COMPANY)

    def click_careers_button(self):
        """
        Clicks 'Careers' button under 'Company' dropdown

        """
        self.click_element(*self.CATEGORY_CAREERS)
