from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
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

    EXACT_ADD_BUTTON = (
        By.XPATH,
        "(//button[@aria-label='Add' and .//span[normalize-space()='Add']])[1]"
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
        "//*[contains(text(),'YOUR CART IS EMPTY') or contains(text(),'Your cart is empty') or contains(text(),'empty') or contains(text(),'Empty')]"
    )

    PROCEED_BUTTON = (
        By.XPATH,
        "//button[@title='Proceed' and @aria-label='Button' and .//span[normalize-space()='Proceed']]"
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

                if (
                    text === 'doctor s choice' ||
                    text.includes('doctor s choice')
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
            logger.info("Doctor S Choice filter clicked successfully")
            time.sleep(5)
            return

        raise Exception("Doctor S Choice filter option not found")

    def get_exact_add_button(self):

        logger.info("Finding exact Add button")

        add_button = self.get_element(
            self.EXACT_ADD_BUTTON,
            timeout=20
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_button
        )

        time.sleep(2)

        return add_button

    def get_product_name_from_add_button(self, add_button):

        logger.info("Getting product name from selected Add button")

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
                            !lower.includes('rs') &&
                            !lower.includes('mrp') &&
                            !lower.includes('off') &&
                            !lower.includes('%') &&
                            !lower.includes('rating') &&
                            !lower.includes('cart') &&
                            !lower.includes('bestseller') &&
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

    def click_exact_add_button_once(self, add_button):

        logger.info("Clicking exact Add button one time")

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_button
        )

        time.sleep(1)

        button_text = add_button.text.strip()

        logger.info(f"Add button text before click: {button_text}")

        assert button_text.lower() == "add", \
            "Add button is not available"

        try:
            add_button.click()
            logger.info("Clicked Add using normal Selenium click")
            return

        except Exception as e:
            logger.info(f"Normal Selenium click failed: {e}")

        try:
            ActionChains(self.driver)\
                .move_to_element(add_button)\
                .pause(1)\
                .click(add_button)\
                .perform()

            logger.info("Clicked Add using ActionChains")
            return

        except Exception as e:
            logger.info(f"ActionChains click failed: {e}")

        self.driver.execute_script(
            """
            const button = arguments[0];

            button.scrollIntoView({block:'center'});

            button.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
            button.dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));
            button.dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));
            button.dispatchEvent(new MouseEvent('click', {bubbles: true}));
            """,
            add_button
        )

        logger.info("Clicked Add using JavaScript mouse events")

    def go_to_cart(self):

        logger.info("Opening cart")

        self.close_popup_if_present()

        try:
            self.click(self.CART_ICON, timeout=10)

        except Exception:
            logger.info("Cart icon click failed, opening cart directly")
            self.driver.get("https://www.apollopharmacy.in/cart")

        WebDriverWait(self.driver, 15).until(
            lambda driver:
            "cart" in driver.current_url.lower()
            or len(driver.find_elements(*self.CART_TEXT)) > 0
        )

        time.sleep(5)

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

        time.sleep(3)

        if self.is_cart_empty():
            return False

        cart_text = self.driver.find_element(By.TAG_NAME, "body").text

        if product_name.lower() in cart_text.lower():
            logger.info("Exact product found in cart")
            return True

        logger.error("Exact product not found in cart")
        return False

    def add_exact_product_to_cart_with_retry(self, max_attempts=3):

        logger.info("Adding exact product to cart with retry")

        product_name = None

        for attempt in range(1, max_attempts + 1):

            logger.info(f"Add product attempt: {attempt}")

            self.driver.get(self.HEALTH_MONITORS_URL)

            WebDriverWait(self.driver, 10).until(
                lambda driver:
                "apollo-brand-health-monitors" in driver.current_url
            )

            time.sleep(4)

            self.apply_doctor_s_choice_filter()

            add_button = self.get_exact_add_button()

            product_name = self.get_product_name_from_add_button(add_button)

            logger.info(f"Trying to add product: {product_name}")

            self.click_exact_add_button_once(add_button)

            time.sleep(7)

            self.go_to_cart()

            if (
                self.is_cart_page_opened()
                and self.is_exact_product_present_in_cart(product_name)
            ):
                logger.info("Product added and verified in cart successfully")
                return product_name

            logger.error("Product not found in cart after Add click")

        raise AssertionError(
            f"Product was not added to cart after {max_attempts} attempts"
        )

    def click_proceed_button(self):

        logger.info("Clicking Proceed button on cart page")

        assert self.is_cart_page_opened(), \
            "Cart page is not opened, cannot click Proceed"

        assert not self.is_cart_empty(), \
            "Cart is empty, cannot click Proceed"

        # Proceed button is usually near bottom/right cart summary
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

        time.sleep(3)

        clicked = self.driver.execute_script(
            """
            const elements = Array.from(
                document.querySelectorAll('button, span, div')
            );

            function normalizeText(value) {
                return (value || '')
                    .replace(/\\s+/g, ' ')
                    .trim()
                    .toLowerCase();
            }

            function isVisible(element) {
                const style = window.getComputedStyle(element);
                const rect = element.getBoundingClientRect();

                return (
                    style.display !== 'none' &&
                    style.visibility !== 'hidden' &&
                    rect.width > 0 &&
                    rect.height > 0
                );
            }

            for (const element of elements) {

                if (!isVisible(element)) {
                    continue;
                }

                const text = normalizeText(
                    element.innerText || element.textContent
                );

                const title = normalizeText(
                    element.getAttribute('title')
                );

                if (
                    text === 'proceed' ||
                    title === 'proceed'
                ) {

                    let clickable = element.closest('button');

                    if (!clickable) {
                        clickable = element;
                    }

                    clickable.scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });

                    clickable.dispatchEvent(
                        new MouseEvent('mouseover', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        })
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('mousedown', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        })
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('mouseup', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        })
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('click', {
                            bubbles: true,
                            cancelable: true,
                            view: window
                        })
                    );

                    return true;
                }
            }

            return false;
            """
        )

        assert clicked is True, \
            "Proceed button was not found or not clicked"

        logger.info("Proceed button clicked successfully")

        time.sleep(5)

    def is_after_proceed_page_opened(self):

        logger.info("Checking page after clicking Proceed")

        page_text = self.driver.find_element(By.TAG_NAME, "body").text.lower()
        current_url = self.driver.current_url.lower()

        logger.info(f"Current URL after proceed: {current_url}")

        return (
            "select address" in page_text
            or "delivery address" in page_text
            or "add address" in page_text
            or "address" in page_text
            or "payment" in page_text
            or "login" in page_text
            or "continue" in page_text
            or "checkout" in current_url
            or "address" in current_url
            or "payment" in current_url
            or "cart" not in current_url
        )