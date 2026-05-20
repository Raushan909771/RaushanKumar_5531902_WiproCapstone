from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import StaleElementReferenceException
import time

from pages.basepage import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class LoginPage(BasePage):

    LOGIN_ICON = (
        By.XPATH,
        "//*[contains(text(),'Login') or contains(text(),'Sign in') or contains(text(),'Sign In')]"
    )

    MOBILE_INPUT = (
        By.XPATH,
        "//input"
    )

    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Continue')]"
    )

    OTP_SCREEN_TEXT = (
        By.XPATH,
        "//*[contains(text(),'OTP') or contains(text(),'otp') or contains(text(),'Resend') or contains(text(),'sent')]"
    )

    OTP_INPUTS = (
        By.XPATH,
        "//input"
    )

    VERIFY_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Verify') or contains(text(),'Continue') or contains(text(),'Submit')]"
    )

    def open_login_popup(self):

        logger.info("Opening login popup")

        self.close_popup_if_present()

        time.sleep(2)

        try:
            self.click(self.LOGIN_ICON, timeout=8)
            logger.info("Login clicked using normal Selenium click")
            time.sleep(2)
            return

        except Exception as e:
            logger.info(f"Normal login click failed: {e}")

        try:
            self.js_click(self.LOGIN_ICON, timeout=8)
            logger.info("Login clicked using JavaScript click")
            time.sleep(2)
            return

        except Exception as e:
            logger.info(f"JavaScript login click failed: {e}")

        clicked = self.driver.execute_script(
            """
            const elements = document.querySelectorAll(
                'button, div, span, p, a'
            );

            for (const element of elements) {
                const text = (element.innerText || element.textContent || '')
                    .trim()
                    .toLowerCase();

                if (
                    text === 'login' ||
                    text.includes('login') ||
                    text.includes('sign in')
                ) {
                    element.scrollIntoView({block: 'center'});
                    element.click();
                    return true;
                }
            }

            return false;
            """
        )

        if clicked:
            logger.info("Login clicked using JavaScript text search")
            time.sleep(2)
            return

        raise Exception("Login button not found on Apollo247 homepage")

    def login_with_mobile_number(self, mobile_number):

        logger.info("Starting login with mobile number")

        self.open_login_popup()

        logger.info(f"Entering mobile number automatically: {mobile_number}")

        mobile_box = self.get_element(self.MOBILE_INPUT, timeout=10)

        mobile_box.clear()

        mobile_box.send_keys(mobile_number)

        time.sleep(1)

        logger.info("Clicking Continue button")

        self.click(self.CONTINUE_BUTTON, timeout=10)

        time.sleep(3)

    def is_otp_screen_visible(self):

        logger.info("Checking OTP screen")

        return self.is_visible(self.OTP_SCREEN_TEXT, timeout=10)

    def wait_for_otp_entry_and_submit(self, mobile_number, timeout=60):

        logger.info("Waiting for OTP entry")

        wait = WebDriverWait(
            self.driver,
            timeout,
            ignored_exceptions=(StaleElementReferenceException,)
        )

        def otp_entered(driver):

            try:
                inputs = driver.find_elements(*self.OTP_INPUTS)

                visible_values = []

                for input_box in inputs:
                    try:
                        if input_box.is_displayed():
                            value = input_box.get_attribute("value")

                            if value:
                                visible_values.append(value)

                    except StaleElementReferenceException:
                        return False

                entered_text = "".join(visible_values).strip()

                if entered_text == mobile_number:
                    return False

                if len(entered_text) >= 4:
                    return True

                return False

            except StaleElementReferenceException:
                return False

        wait.until(otp_entered)

        logger.info("OTP entered manually")

        self.submit_otp()

        time.sleep(2)

        return True

    def submit_otp(self):

        logger.info("Submitting OTP")

        try:
            buttons = self.driver.find_elements(*self.VERIFY_BUTTON)

            for button in buttons:
                try:
                    if button.is_displayed() and button.is_enabled():
                        self.driver.execute_script(
                            "arguments[0].click();",
                            button
                        )

                        logger.info("OTP submitted using button")

                        return

                except StaleElementReferenceException:
                    continue

        except Exception as e:
            logger.info(f"OTP submit button not clicked: {e}")

        try:
            inputs = self.driver.find_elements(*self.OTP_INPUTS)

            for input_box in inputs:
                try:
                    if input_box.is_displayed():
                        input_box.send_keys(Keys.ENTER)

                        logger.info("OTP submitted using Enter key")

                        return

                except StaleElementReferenceException:
                    continue

        except Exception as e:
            logger.info(f"OTP Enter key submit failed: {e}")