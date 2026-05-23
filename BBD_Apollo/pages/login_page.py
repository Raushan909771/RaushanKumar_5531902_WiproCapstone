from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
import time

from pages.base_page import BasePage
from locators.login_locators import LoginLocators
from utils.logger import LogGen

logger = LogGen.loggen()


class LoginPage(BasePage):

    def open_login_popup(self):

        logger.info("Opening login popup")

        self.close_popup_if_present()

        time.sleep(2)

        try:
            self.click(LoginLocators.LOGIN_ICON, timeout=8)

            time.sleep(2)

            return

        except Exception as e:
            logger.info(f"Normal login click failed: {e}")

        try:
            self.js_click(LoginLocators.LOGIN_ICON, timeout=8)

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

                const text = (
                    element.innerText ||
                    element.textContent ||
                    ''
                ).trim().toLowerCase();

                if (text.includes('login') || text.includes('sign in')) {
                    element.click();
                    return true;
                }
            }

            return false;
            """
        )

        if not clicked:
            raise Exception("Login button not found")

        time.sleep(2)

    def login_with_mobile_number(self, mobile_number):

        logger.info("Starting login with mobile number")

        self.open_login_popup()

        mobile_input = self.get_element(
            LoginLocators.MOBILE_INPUT,
            timeout=10
        )

        mobile_input.clear()
        mobile_input.send_keys(mobile_number)

        time.sleep(1)

        try:
            self.click(LoginLocators.CONTINUE_BUTTON, timeout=8)

        except Exception:
            mobile_input.send_keys(Keys.ENTER)

        time.sleep(3)

    def is_otp_screen_visible(self):

        logger.info("Checking OTP screen")

        return self.is_visible(
            LoginLocators.OTP_SCREEN_TEXT,
            timeout=10
        )

    def wait_for_otp_entry_and_submit(self, timeout=60):

        logger.info("Waiting for OTP entry")

        end_time = time.time() + timeout

        while time.time() < end_time:

            try:
                inputs = self.driver.find_elements(
                    *LoginLocators.MOBILE_INPUT
                )

                values = [
                    field.get_attribute("value") or ""
                    for field in inputs
                ]

                if any(len(value.strip()) >= 4 for value in values):

                    logger.info("OTP entered manually")

                    try:
                        inputs[-1].send_keys(Keys.ENTER)
                        logger.info("OTP submitted using Enter key")

                    except StaleElementReferenceException:
                        pass

                    time.sleep(2)

                    return True

            except Exception as e:
                logger.info(f"Waiting for OTP: {e}")

            time.sleep(1)

        return False