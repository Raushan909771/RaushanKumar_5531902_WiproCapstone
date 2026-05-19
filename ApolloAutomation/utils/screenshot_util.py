import os
from datetime import datetime

from utils.logger import LogGen

logger = LogGen.loggen()


class ScreenshotUtil:

    @staticmethod
    def capture_screenshot(driver, screenshot_name="screenshot"):

        try:
            logger.info("Starting screenshot capture process")

            base_dir = os.path.dirname(os.path.dirname(__file__))

            screenshot_dir = os.path.join(
                base_dir,
                "reports",
                "screenshots"
            )

            if not os.path.exists(screenshot_dir):
                os.makedirs(screenshot_dir)
                logger.info("Screenshots directory created successfully")

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

            clean_name = (
                screenshot_name
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
                .replace(":", "_")
                .replace("[", "_")
                .replace("]", "_")
                .lower()
            )

            screenshot_path = os.path.join(
                screenshot_dir,
                f"{clean_name}_{timestamp}.png"
            )

            driver.save_screenshot(screenshot_path)

            logger.info(f"Screenshot captured successfully: {screenshot_path}")

            print(f"Screenshot saved: {screenshot_path}")

            return screenshot_path

        except Exception as e:
            logger.error("Failed to capture screenshot")
            logger.error(f"Error: {str(e)}")
            raise