import unittest
import logging
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

BROWSER_OPTIONS = {
    'chrome': [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080"
    ],
    'firefox': [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--window-size=1920,1080"
    ]
}


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


class BaseTest(unittest.TestCase):
    BROWSERS = ['chrome', 'firefox']
    current_browser = 'chrome'  # Default browser

    def get_driver(self):
        """
        Initialize WebDriver instance based on the current browser type

        """
        try:
            if self.current_browser == 'chrome':
                chrome_options = ChromeOptions()
                for option in BROWSER_OPTIONS['chrome']:
                    chrome_options.add_argument(option)

                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)

            elif self.current_browser == 'firefox':
                firefox_options = FirefoxOptions()
                for option in BROWSER_OPTIONS['firefox']:
                    firefox_options.add_argument(option)

                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=firefox_options)
            else:
                raise ValueError(f"Unsupported browser type: {self.current_browser}")

            driver.implicitly_wait(5)  # Consistent with your pytest version
            driver.maximize_window()
            print(f"{self.current_browser.capitalize()} driver initialized successfully")
            return driver

        except Exception as e:
            print(f"Failed to initialize {self.current_browser}: {e}")
            raise

    def setUp(self):
        self.driver = self.get_driver()
        self.logger = init_logger()
        self.logger.info(f"Running tests with{self.current_browser.upper()} browser")
        self.start_time = datetime.utcnow()

    def tearDown(self):
        test_name = self._testMethodName
        if self.driver:
            if hasattr(self, '_outcome'):
                result = self._outcome.result
                if len(result.failures) > 0 or len(result.errors) > 0:
                    self._take_screenshot(test_name)
            self.driver.quit()

    def _take_screenshot(self, test_name):
        """Take screenshot on test failure"""
        if not os.path.exists('screenshots'):
            os.makedirs('screenshots')
        screenshot_path = f"screenshots/{test_name}_{self.current_browser}.png"
        self.driver.save_screenshot(screenshot_path)
        print(f"🖼 Screenshot captured: {screenshot_path}")

    @classmethod
    def run_all_browsers(cls):
        """Run tests for each browser sequentially"""
        results = []
        for browser in cls.BROWSERS:
            print(f"\n{'=' * 50}")
            print(f"Starting tests with {browser.upper()} browser")
            print(f"{'=' * 50}")
            cls.current_browser = browser
            suite = unittest.TestLoader().loadTestsFromTestCase(cls)
            result = unittest.TextTestRunner().run(suite)
            results.append(result.wasSuccessful())

        return all(results)
