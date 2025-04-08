import unittest
import logging
import os
import pytest

from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from database_controller import insert_test_result_to_influxdb


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    return logger


@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    """Start browser and close after testing"""

    if request.param == "chrome":
        chrome_options = ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)

    elif request.param == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)

    driver.maximize_window()
    yield driver
    driver.quit()


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.driver = self.get_driver()
        self.logger = init_logger()
        self.start_time = datetime.utcnow()

    @pytest.hookimpl(tryfirst=True, hookwrapper=True)
    def pytest_runtest_makereport(item):
        """
        Pytest hook to handle test result reporting:
        - Inserts test result to InfluxDB
        - Captures screenshot on test failure

        :param item: pytest test item

        """
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            test_name = item.name
            status = "passed" if report.passed else "failed"
            duration = getattr(report, 'duration', 0)
            timestamp = datetime.utcnow()

            try:
                insert_test_result_to_influxdb(
                    test_name=test_name,
                    status=status,
                    duration=duration,
                    timestamp=timestamp
                )
            except Exception as e:
                print(f"❌ Error writing to InfluxDB: {e}")

            """" # If the test fails, take a screenshot."""
            if report.failed:
                driver = item.funcargs.get("driver", None)
                if driver:
                    screenshot_dir = "screenshots"
                    os.makedirs(screenshot_dir, exist_ok=True)
                    screenshot_path = os.path.join(screenshot_dir, f"{test_name}.png")
                    driver.save_screenshot(screenshot_path)
                    print(f"🖼 Ekran görüntüsü alındı: {screenshot_path}")
