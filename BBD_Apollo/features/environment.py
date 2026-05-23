import os
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


def before_all(context):

    logger.info("=======================================")
    logger.info("BDD AUTOMATION EXECUTION STARTED")

    browser = ConfigReader.get_browser().strip().lower()
    headless = ConfigReader.is_headless()

    logger.info(f"Browser from config: {browser}")
    logger.info(f"Headless mode: {headless}")

    if browser == "chrome":

        chrome_options = ChromeOptions()

        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        if headless:
            chrome_options.add_argument("--headless=new")

        context.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=chrome_options
        )

    else:

        raise Exception("Only Chrome browser is supported")

    context.driver.maximize_window()

    logger.info("Chrome browser launched successfully")


def before_scenario(context, scenario):

    logger.info("------------------------------------------------")
    logger.info(f"Scenario started: {scenario.name}")
    logger.info("------------------------------------------------")


def attach_log_to_allure(scenario_name):

    try:

        log_path = os.path.join(
            os.getcwd(),
            "logs",
            "automation.log"
        )

        if os.path.exists(log_path):

            allure.attach.file(
                log_path,
                name=f"LOG_{scenario_name}",
                attachment_type=allure.attachment_type.TEXT
            )

            logger.info("Log file attached to Allure report")

        else:

            logger.info("Log file not found, skipping Allure log attachment")

    except Exception as e:

        logger.info(f"Failed to attach log to Allure report: {e}")


def after_scenario(context, scenario):

    safe_name = (
        scenario.name
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(":", "_")
        .lower()
    )

    logger.info("------------------------------------------------")
    logger.info(f"Scenario finished: {scenario.name}")
    logger.info(f"Scenario status: {scenario.status.name}")
    logger.info("------------------------------------------------")

    if scenario.status.name == "passed":

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver,
            f"passed_{safe_name}"
        )

    else:

        screenshot_path = ScreenshotUtil.capture_screenshot(
            context.driver,
            f"failed_{safe_name}"
        )

    try:

        with open(screenshot_path, "rb") as image_file:

            allure.attach(
                image_file.read(),
                name=f"SCREENSHOT_{safe_name}",
                attachment_type=allure.attachment_type.PNG
            )

        logger.info("Screenshot attached to Allure report")

    except Exception as e:

        logger.info(f"Allure screenshot attachment skipped: {e}")

    attach_log_to_allure(safe_name)


def after_all(context):

    logger.info("Waiting 6 seconds before closing browser")

    time.sleep(6)

    context.driver.quit()

    logger.info("Browser closed successfully")
    logger.info("BDD AUTOMATION EXECUTION FINISHED")
    logger.info("============================================")