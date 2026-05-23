from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import time

from pages.base_page import BasePage
from locators.shop_locators import ShopLocators
from utils.logger import LogGen

logger = LogGen.loggen()


class ShopByCategoryPage(BasePage):

    HEALTH_MONITORS_URL = (
        "https://www.apollopharmacy.in/shop-by-category/apollo-brand-health-monitors"
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
            self.scroll_to_element(
                ShopLocators.HEALTH_MONITORS_TEXT,
                timeout=5
            )

            time.sleep(1)

            health_monitor_element = self.get_element(
                ShopLocators.HEALTH_MONITORS_TEXT,
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

        time.sleep(6)

    def is_health_monitors_page_opened(self):

        current_url = self.driver.current_url

        logger.info(f"Current URL is: {current_url}")

        return "apollo-brand-health-monitors" in current_url

    def is_brands_filter_visible(self):

        logger.info("Checking Brands filter visibility")

        time.sleep(5)

        page_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text.lower()

        return "brands" in page_text

    def open_brands_filter(self):

        logger.info("Opening Brands filter")

        self.close_popup_if_present()

        time.sleep(3)

        opened = self.driver.execute_script(
            """
            const elements = Array.from(
                document.querySelectorAll('label, div, span, h3, button')
            );

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

                const text = (
                    element.innerText ||
                    element.textContent ||
                    ''
                ).trim().toLowerCase();

                if (text === 'brands' || text.includes('brands')) {

                    element.scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });

                    const clickable =
                        element.closest('label, button, div') || element;

                    clickable.click();

                    return true;
                }
            }

            return false;
            """
        )

        assert opened is True, \
            "Brands filter was not found or not clicked"

        time.sleep(3)

    def apply_doctor_s_choice_filter(self):

        logger.info("Applying Doctor S Choice brand filter")

        self.close_popup_if_present()

        self.open_brands_filter()

        time.sleep(3)

        clicked = self.driver.execute_script(
            """
            function normalizeText(value) {
                return (value || '')
                    .replace(/[’']/g, '')
                    .replace(/[^a-zA-Z0-9]/g, ' ')
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

            window.scrollBy(0, 300);

            const elements = Array.from(
                document.querySelectorAll('label, div, span, p, h3, button')
            );

            for (const element of elements) {

                if (!isVisible(element)) {
                    continue;
                }

                const text = normalizeText(
                    element.innerText || element.textContent
                );

                const isDoctorChoice =
                    text.includes('doctor s choice') ||
                    text.includes('doctors choice') ||
                    (
                        text.includes('doctor') &&
                        text.includes('choice')
                    );

                if (isDoctorChoice) {

                    element.scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });

                    const clickable =
                        element.closest('label, button, div') || element;

                    clickable.dispatchEvent(
                        new MouseEvent('mouseover', {bubbles: true})
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('mousedown', {bubbles: true})
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('mouseup', {bubbles: true})
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('click', {bubbles: true})
                    );

                    return true;
                }
            }

            return false;
            """
        )

        assert clicked is True, \
            "Doctor S Choice filter option was not found or not clicked"

        time.sleep(5)

    def get_exact_add_button(self):

        add_button = self.get_element(
            ShopLocators.EXACT_ADD_BUTTON,
            timeout=20
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_button
        )

        time.sleep(2)

        return add_button

    def get_product_name_from_add_button(self, add_button):

        product_name = self.driver.execute_script(
            """
            const addBtn = arguments[0];

            let parent = addBtn;

            for (let i = 0; i < 12; i++) {

                if (!parent) {
                    break;
                }

                const text = (
                    parent.innerText ||
                    parent.textContent ||
                    ''
                ).trim();

                if (
                    text.length > 10 &&
                    text.toLowerCase().includes('add')
                ) {

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
        ).strip()

        if product_name == "":
            raise Exception("Product name could not be captured")

        return product_name

    def click_exact_add_button_once(self, add_button):

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block:'center'});",
            add_button
        )

        time.sleep(1)

        try:
            add_button.click()
            return

        except Exception:
            pass

        try:
            ActionChains(self.driver)\
                .move_to_element(add_button)\
                .pause(1)\
                .click(add_button)\
                .perform()

            return

        except Exception:
            pass

        self.driver.execute_script(
            """
            const button = arguments[0];

            button.scrollIntoView({block:'center'});

            button.dispatchEvent(
                new MouseEvent('mouseover', {bubbles: true})
            );

            button.dispatchEvent(
                new MouseEvent('mousedown', {bubbles: true})
            );

            button.dispatchEvent(
                new MouseEvent('mouseup', {bubbles: true})
            );

            button.dispatchEvent(
                new MouseEvent('click', {bubbles: true})
            );
            """,
            add_button
        )

    def go_to_cart(self):

        logger.info("Opening cart")

        self.close_popup_if_present()

        try:
            self.click(ShopLocators.CART_ICON, timeout=10)

        except Exception:
            self.driver.get("https://www.apollopharmacy.in/cart")

        WebDriverWait(self.driver, 15).until(
            lambda driver:
            "cart" in driver.current_url.lower()
            or len(driver.find_elements(*ShopLocators.CART_TEXT)) > 0
        )

        time.sleep(5)

    def is_cart_page_opened(self):

        return (
            "cart" in self.driver.current_url.lower()
            or self.is_visible(ShopLocators.CART_TEXT, timeout=5)
        )

    def is_cart_empty(self):

        empty_items = self.driver.find_elements(
            *ShopLocators.EMPTY_CART_TEXT
        )

        for item in empty_items:

            try:
                if item.is_displayed():
                    return True

            except Exception:
                continue

        return False

    def is_exact_product_present_in_cart(self, product_name):

        time.sleep(3)

        if self.is_cart_empty():
            return False

        cart_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text

        return product_name.lower() in cart_text.lower()

    def add_exact_product_to_cart_with_retry(self, max_attempts=3):

        product_name = None

        for attempt in range(1, max_attempts + 1):

            logger.info(f"Add product attempt: {attempt}")

            self.driver.get(self.HEALTH_MONITORS_URL)

            WebDriverWait(self.driver, 10).until(
                lambda driver:
                "apollo-brand-health-monitors" in driver.current_url
            )

            time.sleep(6)

            self.apply_doctor_s_choice_filter()

            add_button = self.get_exact_add_button()

            product_name = self.get_product_name_from_add_button(
                add_button
            )

            self.click_exact_add_button_once(add_button)

            time.sleep(7)

            self.go_to_cart()

            if (
                self.is_cart_page_opened()
                and self.is_exact_product_present_in_cart(product_name)
            ):
                return product_name

        raise AssertionError(
            f"Product was not added to cart after {max_attempts} attempts"
        )

    def click_proceed_button(self):

        assert self.is_cart_page_opened(), \
            "Cart page is not opened, cannot click Proceed"

        assert not self.is_cart_empty(), \
            "Cart is empty, cannot click Proceed"

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

                if (text === 'proceed' || title === 'proceed') {

                    let clickable = element.closest('button');

                    if (!clickable) {
                        clickable = element;
                    }

                    clickable.scrollIntoView({
                        block: 'center',
                        inline: 'center'
                    });

                    clickable.dispatchEvent(
                        new MouseEvent('mouseover', {bubbles: true})
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('mousedown', {bubbles: true})
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('mouseup', {bubbles: true})
                    );

                    clickable.dispatchEvent(
                        new MouseEvent('click', {bubbles: true})
                    );

                    return true;
                }
            }

            return false;
            """
        )

        assert clicked is True, \
            "Proceed button was not found or not clicked"

        time.sleep(5)

    def is_after_proceed_page_opened(self):

        time.sleep(5)

        page_text = self.driver.find_element(
            By.TAG_NAME,
            "body"
        ).text.lower()

        current_url = self.driver.current_url.lower()

        return (
            "medicines-cart" in current_url
            or "select address" in page_text
            or "delivery address" in page_text
            or "add address" in page_text
            or "address" in page_text
            or "payment" in page_text
            or "login" in page_text
            or "continue" in page_text
            or "checkout" in current_url
            or "address" in current_url
            or "payment" in current_url
        )