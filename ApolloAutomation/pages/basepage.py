
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.logger import LogGen

logger = LogGen.loggen()


class BasePage:

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def get_element(self, locator, condition=EC.visibility_of_element_located, timeout=20):
        logger.info(f"Locating the element: {locator}")
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(condition(locator))

    def click(self, locator, timeout=10):
        logger.info(f"Clicking the element: {locator}")
        self.get_element(locator, EC.element_to_be_clickable, timeout).click()

    def type(self, locator, text, timeout=10):
        logger.info(f"Typing into element: {locator}")
        element = self.get_element(locator, EC.visibility_of_element_located, timeout)
        element.clear()
        element.send_keys(text)

    def is_visible(self, locator, timeout=5):
        logger.info(f"Checking visibility of element: {locator}")

        try:
            return self.get_element(
                locator,
                EC.visibility_of_element_located,
                timeout
            ).is_displayed()
        except:
            return False

    def scroll_to_element(self, locator, timeout=10):
        logger.info(f"Scrolling to element: {locator}")

        element = self.get_element(
            locator,
            EC.visibility_of_element_located,
            timeout
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            element
        )

    def js_click(self, locator, timeout=10):
        logger.info(f"Clicking element using JavaScript: {locator}")

        element = self.get_element(
            locator,
            EC.visibility_of_element_located,
            timeout
        )

        self.driver.execute_script(
            "arguments[0].click();",
            element
        )

    def close_popup_if_present(self):
        logger.info("Checking popup on page")

        self.driver.execute_script("""
            const popup = document.querySelector('ct-web-popup-imageonly');
            if (popup) {
                popup.remove();
            }

            const closeButtons = document.querySelectorAll(
                '[class*="close"], [aria-label*="close"], [aria-label*="Close"]'
            );

            closeButtons.forEach(button => {
                try {
                    button.click();
                } catch(e) {}
            });
        """)