import pytest
import time
import allure

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from webdriver_manager.chrome import ChromeDriverManager

from utils.config_reader import ConfigReader
from utils.logger import LogGen
from utils.screenshot_util import ScreenshotUtil

logger = LogGen.loggen()


@pytest.fixture(scope="session")
def driver():

    browser = ConfigReader.get("browser").strip().lower()

    logger.info("=======================================")
    logger.info("Starting test session")
    logger.info("Reading Configuration")

    print(f"Browser from config: '{browser}'")

    logger.info(f"Browser from config : {browser}")

    base_url = ConfigReader.get("base_url").strip()

    logger.info(f"Base URL From Config : {base_url}")

    headless = ConfigReader.get("headless").strip().lower() == "true"

    logger.info(f"Headless : {headless}")

    if browser == "chrome":

        chrome_options = ChromeOptions()

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        if headless:
            chrome_options.add_argument("--headless=new")

        driver = webdriver.Chrome(
            service=ChromeService(
                ChromeDriverManager().install()
            ),
            options=chrome_options
        )

    else:
        raise Exception("Only Chrome browser is supported for this project")

    logger.info(f"Open Browser : {browser}")

    driver.get(base_url)

    logger.info(f"URL Loaded : {base_url}")

    yield driver

    logger.info("Waiting 6 seconds before closing browser")

    time.sleep(6)

    driver.quit()

    logger.info("Closing the browser")
    logger.info("Ending test session")
    logger.info("============================================")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):

    outcome = yield

    report = outcome.get_result()

    if report.when == "call":

        driver = item.funcargs.get("driver", None)

        if driver is not None:

            test_name = item.name

            if report.passed:

                logger.info(f"Test passed: {test_name}")

                screenshot_path = ScreenshotUtil.capture_screenshot(
                    driver,
                    f"passed_{test_name}"
                )

                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"PASSED_{test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )

            elif report.failed:

                logger.error(f"Test failed: {test_name}")

                screenshot_path = ScreenshotUtil.capture_screenshot(
                    driver,
                    f"failed_{test_name}"
                )

                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"FAILED_{test_name}",
                        attachment_type=allure.attachment_type.PNG
                    )