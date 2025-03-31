from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CareersPage(BasePage):
    OUR_LOCATIONS = (By.ID, 'career-our-location')
    TEAMS = (By.LINK_TEXT, 'See all teams')
    LIFE_AT_INSIDER = (By.XPATH, "//h2[contains(text(), 'Life at Insider')]")



