from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class BasePage(object):
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 20)

    def click_element(self, *locator):
        """
        Clicks to given element as locator

        """
        self.driver.find_element(*locator).click()

    def hover_element(self, *locator):
        """
        Hovers to given element as locator

        """
        element = self.driver.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def get_current_url(self):
        """
        Returns current url of browser

        """
        return self.driver.current_url

    def wait_element(self, method, message=''):
        """
        Waits and then returns for a curtain element to be clickable

        """
        return self.wait.until(ec.element_to_be_clickable(method), message)

    def get_text(self, locator):
        """
        Returns raw text of given element as locator

        """
        return self.wait_element(locator).text

    def get_cleaned_text(self, locator):
        """
        Returns text of given element with special characters and extra whitespace removed

        """
        text = self.wait_element(locator).text
        return text.replace('×\n', '').strip()

    def verify_element_visibility(self, locator, message=''):
        """
        Returns true if element is visible

        """
        return self.wait.until(ec.visibility_of_element_located(locator), message)

    def go_to_url(self, url):
        """
        Goes to a website that is given in base_url

        """
        self.driver.get(url)
