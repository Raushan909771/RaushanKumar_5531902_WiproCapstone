from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time

from pages.basepage import BasePage
from utils.logger import LogGen

logger = LogGen.loggen()


class ShopByCategoryPage(BasePage):

    HEALTH_MONITORS_TEXT = (
        By.XPATH,
        "//*[normalize-space()='Health Monitors']"
    )

    HEALTH_MONITORS_URL = (
        "https://www.apollopharmacy.in/shop-by-category/apollo-brand-health-monitors"
    )

    BRANDS_FILTER = (
        By.XPATH,
        "//label[@for='checkboxcategory0']"
    )

    BRANDS_FILTER_TITLE = (
        By.XPATH,
        "//label[@for='checkboxcategory0']//h3[normalize-space()='Brands']"
    )

    ADD_BUTTONS = (
        By.XPATH,
        "//button[@aria-label='Add' and .//span[normalize-space()='Add']]"
    )

    CART_ICON = (
        By.XPATH,
        "//*[contains(@href,'cart') or contains(@class,'cart') or contains(text(),'Cart')]"
    )

    CART_TEXT = (
        By.XPATH,
        "//*[contains(text(),'Cart') or contains(text(),'cart')]"
    )

    EMPTY_CART_TEXT = (
        By.XPATH,
        "//*[contains(text(),'empty') or contains(text(),'Empty') or contains(text(),'Your cart is empty')]"
    )

    def is_category_visible(self, category_name, timeout=5):

        self.close_popup_if_present()

        locator = (
            By.XPATH,
            f"//*[normalize-space()='{category_name}']"
        )

        return self.is_visible(locator, timeout=timeout)

    def click_health_monitors(self):

        logger.info("Opening Health Monitors category")

        self.close_popup_if_present()

        try:
            self.scroll_to_element(self.HEALTH_MONITORS_TEXT, timeout=5)

            time.sleep(1)

            health_monitor_element = self.get_element(
                self.HEALTH_MONITORS_TEXT,
                timeout=5
            )

            self.driver.execute_script(
                "arguments[0].click();",
                health_monitor_element
            )

            WebDriverWait(self.driver, 5).until(
                lambda driver:
                "apollo-brand-health-monitors" in driver.current_url
            )

        except Exception as e:

            logger.info(f"Health Monitors click failed: {e}")
            logger.info("Opening Health Monitors page directly")

            self.driver.get(self.HEALTH_MONITORS_URL)

            WebDriverWait(self.driver, 10).until(
                lambda driver:
                "apollo-brand-health-monitors" in driver.current_url
            )

        time.sleep(4)

    def is_health_monitors_page_opened(self):

        logger.info("Validating Health Monitors page")

        current_url = self.driver.current_url

        logger.info(f"Current URL is: {current_url}")

        return "apollo-brand-health-monitors" in current_url

    def is_brands_filter_visible(self):

        logger.info("Checking Brands filter visibility")

        return self.is_visible(self.BRANDS_FILTER_TITLE, timeout=10)

    def open_brands_filter(self):

        logger.info("Opening Brands filter")

        self.close_popup_if_present()

        self.scroll_to_element(self.BRANDS_FILTER, timeout=10)

        try:
            self.click(self.BRANDS_FILTER, timeout=5)

        except Exception:
            logger.info("Normal Brands filter click failed, trying JavaScript click")
            self.js_click(self.BRANDS_FILTER, timeout=5)

        time.sleep(2)

    def apply_doctor_s_choice_filter(self):

        logger.info("Applying Doctor S Choice brand filter")

        self.close_popup_if_present()

        self.open_brands_filter()

        time.sleep(1)

        clicked = self.driver.execute_script(
            """
            const allElements = document.querySelectorAll('label, div, span');

            for (const element of allElements) {
                const text = (element.innerText || element.textContent || '')
                    .trim()
                    .toLowerCase();

                if (text === 'doctor s choice' || text.includes('doctor s choice')) {
                    element.scrollIntoView({block: 'center'});
                    element.click();
                    return true;
                }
            }

            return false;
            """
        )

        if clicked:
            logger.info("Doctor S Choice filter clicked successfully")
            time.sleep(5)
            return

        raise Exception("Doctor S Choice filter option not found")

    def get_first_available_add_button(self):

        logger.info("Finding first available Add button")

        WebDriverWait(self.driver, 15).until(
            lambda driver:
            len(driver.find_elements(*self.ADD_BUTTONS)) > 0
        )

        add_buttons = self.driver.find_elements(*self.ADD_BUTTONS)

        for button in add_buttons:

            try:
                if button.is_displayed() and button.is_enabled():

                    button_text = button.text.strip().lower()

                    if button_text == "add":

                        logger.info("Available Add button found")

                        return button

            except Exception:
                continue

        raise Exception("No available Add button found")

    def get_product_name_from_add_button(self, add_button):

        logger.info("Getting product name from selected product card")

        product_name = self.driver.execute_script(
            """
            const addBtn = arguments[0];

            let parent = addBtn;

            for (let i = 0; i < 12; i++) {

                if (!parent) {
                    break;
                }

                const text = (parent.innerText || parent.textContent || '').trim();

                if (text.length > 10 && text.toLowerCase().includes('add')) {

                    const lines = text
                        .split('\\n')
                        .map(line => line.trim())
                        .filter(line => line.length > 0);

                    for (const line of lines) {

                        const lower = line.toLowerCase();

                        if (
                            !lower.includes('add') &&
                            !lower.includes('₹') &&
                            !lower.includes('mrp') &&
                            !lower.includes('off') &&
                            !lower.includes('%') &&
                            !lower.includes('rating') &&
                            line.length > 5
                        ) {
                            return line;
                        }
                    }
                }

                parent = parent.parentElement;
            }

            return '';
            """,
            add_button
        )

        product_name = product_name.strip()

        logger.info(f"Selected product name: {product_name}")

        if product_name == "":
            raise Exception("Product name could not be captured")

        return product_name

    def add_one_doctor_s_choice_product_to_cart(self):

        logger.info("Adding one Doctor S Choice product to cart")

        self.close_popup_if_present()

        add_button = self.get_first_available_add_button()

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_button
        )

        time.sleep(1)

        product_name = self.get_product_name_from_add_button(add_button)

        logger.info(f"Product selected for cart: {product_name}")

        try:
            add_button.click()

        except Exception:
            logger.info("Normal Add click failed, trying JavaScript click")

            self.driver.execute_script(
                "arguments[0].click();",
                add_button
            )

        logger.info("Clicked Add button only once")

        time.sleep(5)

        return product_name

    def go_to_cart(self):

        logger.info("Opening cart")

        self.close_popup_if_present()

        try:
            self.click(self.CART_ICON, timeout=10)

        except Exception:
            logger.info("Cart icon click failed, opening cart directly")
            self.driver.get("https://www.apollopharmacy.in/cart")

        WebDriverWait(self.driver, 10).until(
            lambda driver:
            "cart" in driver.current_url.lower()
            or len(driver.find_elements(*self.CART_TEXT)) > 0
        )

        time.sleep(3)

    def is_cart_page_opened(self):

        logger.info("Checking cart page")

        return (
            "cart" in self.driver.current_url.lower()
            or self.is_visible(self.CART_TEXT, timeout=5)
        )

    def is_cart_empty(self):

        logger.info("Checking whether cart is empty")

        empty_items = self.driver.find_elements(*self.EMPTY_CART_TEXT)

        for item in empty_items:

            try:
                if item.is_displayed():
                    logger.error("Cart is empty")
                    return True

            except Exception:
                continue

        return False

    def is_exact_product_present_in_cart(self, product_name):

        logger.info(f"Checking exact product in cart: {product_name}")

        time.sleep(2)

        if self.is_cart_empty():
            return False

        cart_text = self.driver.find_element(By.TAG_NAME, "body").text

        logger.info(f"Cart page text: {cart_text}")

        if product_name.lower() in cart_text.lower():
            logger.info("Exact product found in cart")
            return True

        logger.error("Exact product not found in cart")
        return False