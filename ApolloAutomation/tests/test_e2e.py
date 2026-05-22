import pytest
import allure

from pages.loginpage import LoginPage
from pages.shopbycategorypage import ShopByCategoryPage
from utils.csv_reader import CSVReader
from utils.config_reader import ConfigReader
from utils.logger import LogGen

logger = LogGen.loggen()


@pytest.mark.order(1)
@pytest.mark.parametrize(
    "data",
    CSVReader.read_csv("login_data.csv")
)
def test_login(driver, data):

    driver.get(ConfigReader.get("base_url"))

    login_page = LoginPage(driver)

    mobile_number = data["mobile_number"]

    logger.info(f"Trying login with mobile number: {mobile_number}")

    login_page.login_with_mobile_number(mobile_number)

    assert login_page.is_otp_screen_visible(), \
        "OTP screen should be visible after entering mobile number"

    print("\nEnter OTP manually in browser.")
    print("Do not press anything in terminal.")
    print("Automation will continue automatically after OTP is entered.")
    print("Maximum wait time is 60 seconds.\n")

    otp_submitted = login_page.wait_for_otp_entry_and_submit(
        mobile_number,
        timeout=30
    )

    assert otp_submitted is True, \
        "OTP was not entered or submitted"

    logger.info("OTP entered and submitted successfully")


@allure.epic("Apollo247 Automation")
@allure.feature("Shop By Category")
@allure.story("Open Health Monitors")
@pytest.mark.order(3)
def test_click_health_monitors_category(driver):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    shop_by_category_page.click_health_monitors()

    assert shop_by_category_page.is_health_monitors_page_opened(), \
        "Health Monitors page did not open"


@allure.epic("Apollo247 Automation")
@allure.feature("Health Monitors")
@allure.story("Apply Doctor S Choice Filter")
@pytest.mark.order(4)
def test_apply_doctor_s_choice_filter_after_health_monitors(driver):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    shop_by_category_page.click_health_monitors()

    assert shop_by_category_page.is_health_monitors_page_opened(), \
        "Health Monitors page did not open"

    assert shop_by_category_page.is_brands_filter_visible(), \
        "Brands filter is not visible"

    shop_by_category_page.apply_doctor_s_choice_filter()

    assert shop_by_category_page.is_health_monitors_page_opened(), \
        "Health Monitors page is not opened after applying Doctor S Choice filter"


@allure.epic("Apollo247 Automation")
@allure.feature("Cart")
@allure.story("Add Exact Doctor S Choice Product To Cart")
@pytest.mark.order(5)
def test_add_doctor_s_choice_product_to_cart(driver):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    product_name = shop_by_category_page.add_exact_product_to_cart_with_retry(
        max_attempts=3
    )

    assert product_name is not None, \
        "Product name was not captured"

    assert shop_by_category_page.is_cart_page_opened(), \
        "Cart page did not open"

    assert shop_by_category_page.is_exact_product_present_in_cart(product_name), \
        f"Expected product not found in cart: {product_name}"


@allure.epic("Apollo247 Automation")
@allure.feature("Cart")
@allure.story("Proceed After Adding Product To Cart")
@pytest.mark.order(6)
def test_proceed_after_adding_product_to_cart(driver):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    product_name = shop_by_category_page.add_exact_product_to_cart_with_retry(
        max_attempts=3
    )

    assert product_name is not None, \
        "Product name was not captured"

    assert shop_by_category_page.is_cart_page_opened(), \
        "Cart page did not open"

    assert shop_by_category_page.is_exact_product_present_in_cart(product_name), \
        f"Expected product not found in cart: {product_name}"

    shop_by_category_page.click_proceed_button()

    assert shop_by_category_page.is_after_proceed_page_opened(), \
        "Page did not move forward after clicking Proceed"