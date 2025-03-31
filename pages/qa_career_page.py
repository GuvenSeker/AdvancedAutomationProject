import time

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class QaCareerPage(BasePage):
    SEE_ALL_QA_JOBS_BUTTON = (By.LINK_TEXT, 'See all QA jobs')
    FILTER_BY_LOCATION = (By.ID, 'select2-filter-by-location-container')
    FILTER_OPTION_ISTANBUL_TURKIYE = (By.CSS_SELECTOR, '.select2-results__option:nth-of-type(2)')
    FILTER_BY_DEPARTMENT = (By.ID, 'select2-filter-by-department-container')
    SHOWING_LISTING = (By.CLASS_NAME, 'currentResult')
    JOB_TITLE = (By.CSS_SELECTOR, '.position-title')
    JOB_DEPARTMENT = (By.CSS_SELECTOR, '.position-department')
    JOB_LOCATION = (By.CSS_SELECTOR, '.position-location')
    JOB_LIST = (By.CSS_SELECTOR, '.position-list-item')
    VIEW_ROLE_BUTTON = (By.LINK_TEXT, 'View Role')
    qa_website_url = 'https://useinsider.com/careers/quality-assurance/'
    lever_application = 'lever'
    EXPECTED_POSITION = "Quality Assurance"
    EXPECTED_DEPARTMENT = "Quality Assurance"
    EXPECTED_LOCATION = "Istanbul, Turkey"

    def click_see_all_jobs_button(self):
        """
        Clicks 'See All Jobs' button in Quality Assurance Page

        """
        self.click_element(*self.SEE_ALL_QA_JOBS_BUTTON)

    def click_filter_by_location(self):
        """
        Clicks 'Filter by location' dropdown in Quality Assurance Page

        """
        self.click_element(*self.FILTER_BY_LOCATION)

    def select_location_option(self, *location_element):
        """
        Clicks 'Filter by location' dropdown in Quality Assurance Page
        :param str location_element : Location that wanted to be selected

        """
        self.click_element(*location_element)

    def get_job_title_text(self):
        """
        Returns job title text

        """
        job_title_text = self.get_text(self.JOB_TITLE)
        return job_title_text

    def get_job_department_text(self):
        """
        Returns job department text

        """
        job_department_text = self.get_text(self.JOB_DEPARTMENT)
        return job_department_text

    def get_job_location_text(self):
        """
        Returns job location text

        """
        job_location_text = self.get_text(self.JOB_LOCATION)
        return job_location_text

    def click_view_role(self):
        """
        Clicks view role button on listed job

        """
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
        time.sleep(1)
        self.hover_element(*self.JOB_TITLE)
        time.sleep(1)
        self.click_element(*self.VIEW_ROLE_BUTTON)

    def switch_tab(self):
        """
        Switches to new tab

        """
        new_url = self.driver.window_handles[1]
        self.driver.switch_to.window(new_url)

    def verify_all_job_positions(self):
        """
        Verifies all listed jobs have:
        - "Quality Assurance" or "QA" in Position field
        - "Quality Assurance" in Department field
        - "Istanbul, Turkey" in Location field
        Returns: True if all jobs match criteria, False otherwise

        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight * 0.3);")
        time.sleep(2)
        job_items = self.driver.find_elements(*self.JOB_LIST)
        for job in job_items:
            title = job.find_element(*self.JOB_TITLE).text
            department = job.find_element(*self.JOB_DEPARTMENT).text
            location = job.find_element(*self.JOB_LOCATION).text.replace('Turkiye', 'Turkey')

            if not (
                    (self.EXPECTED_POSITION in title or "QA" in title) and
                    self.EXPECTED_DEPARTMENT in department and
                    self.EXPECTED_LOCATION in location
            ):
                print(f"""
                Job position validation failed:
                Expected Position (should contain): {self.EXPECTED_POSITION}, Found: {title}
                Expected Department: {self.EXPECTED_DEPARTMENT}, Found: {department}
                Expected Location: {self.EXPECTED_LOCATION}, Found: {location}
                """)
                return False
        return True

    def get_department_text(self):
        """
        Returns cleaned department text
        
        """
        return self.get_cleaned_text(self.FILTER_BY_DEPARTMENT)
