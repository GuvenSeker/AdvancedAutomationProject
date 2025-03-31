import time

from pages.careers_page import CareersPage
from pages.home_page import HomePage
from pages.qa_career_page import QaCareerPage
from tests.base_test import BaseTest


class AdvancedAutomationPath(BaseTest):
    """
    Test case for verifying the advanced automation path:
    1. Navigate to Insider's Homepage to verify its accessibility.
    2. From the navigation bar, select "Company", then "Careers" and verify if the Career page,
       including its Locations, Teams, and Life at Insider sections, are accessible.
    3. Visit the Quality Assurance Careers Page, click "See all QA jobs",
       filter the jobs by location (Istanbul, Turkey) and department (Quality Assurance),
       and check for the job listings' presence.
    4. Ensure each job position lists "Quality Assurance" in both the Position and Department fields
       and "Istanbul, Turkey" in the Location field.
    5. Verify that clicking the "View Role" button redirects to the Lever Application form page.

    """

    def test_check_advanced_automation_path(self):
        """Test checks advanced automation path"""
        self.logger.info("1. Navigate to Insider's Homepage to verify its accessibility.")
        home_page = HomePage(self.driver)
        home_page.go_to_url(home_page.website_url)
        self.assertEqual(home_page.website_url, home_page.get_current_url(), 'You are not on Insider homepage.')
        self.logger.info("Insider website has opened successfully!")

        self.logger.info("2. From the navigation bar, select 'Company', then 'Careers' and verify sections.")
        home_page.hover_company_from_navigation_bar()
        home_page.click_careers_button()
        careers_page = CareersPage(self.driver)
        careers_page.verify_element_visibility(careers_page.OUR_LOCATIONS)
        self.assertTrue(careers_page.verify_element_visibility(careers_page.OUR_LOCATIONS),
                        "locations can not be found")
        self.assertTrue(careers_page.verify_element_visibility(careers_page.TEAMS), "teams can not be found")
        self.assertTrue(careers_page.verify_element_visibility(careers_page.LIFE_AT_INSIDER),
                        "life at insider can not be found")
        self.logger.info("'Career' page under 'Company' is verified successfully!")

        self.logger.info("3. Visit the Quality Assurance Careers Page, click 'See all QA jobs',"
                         "filter the jobs by location (Istanbul, Turkey) and department (Quality Assurance),"
                         "and check for the job listings presence.")
        qa_career_page = QaCareerPage(self.driver)
        careers_page.go_to_url(qa_career_page.qa_website_url)
        self.assertIn(qa_career_page.qa_website_url, careers_page.get_current_url(), 'You are not on QA page.')
        qa_career_page.click_see_all_jobs_button()
        time.sleep(10)
        qa_career_page.click_filter_by_location()
        qa_career_page.select_location_option(*qa_career_page.FILTER_OPTION_ISTANBUL_TURKIYE)
        self.assertEqual(qa_career_page.get_department_text(), "Quality Assurance", 'QA department is not selected')
        self.assertTrue(qa_career_page.verify_element_visibility(qa_career_page.SHOWING_LISTING), "Jobs are not listed")
        self.logger.info("Jobs listed successfully!")

        self.logger.info("4. Ensure each job position lists 'Quality Assurance' in both the Position "
                         "and Department fields and 'Istanbul, Turkey' in the Location field.")
        time.sleep(1)
        self.assertTrue(qa_career_page.verify_all_job_positions(), "Not all jobs match the required criteria")
        self.logger.info("All jobs verified successfully!")

        self.logger.info("5. Verify that clicking the 'View Role' button redirects to the Lever Application form page.")
        qa_career_page.click_view_role()
        time.sleep(1)
        qa_career_page.switch_tab()
        self.assertIn(qa_career_page.lever_application, qa_career_page.get_current_url(),
                      "You are not on Lever Application form")
        self.logger.info("Lever Application page opened successfully!")
