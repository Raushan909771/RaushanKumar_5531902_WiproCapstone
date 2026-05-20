import pytest
import allure

from pages.shopbycategorypage import ShopByCategoryPage
from utils.csv_reader import CSVReader
from utils.config_reader import ConfigReader


@allure.epic("Apollo247 Automation")
@allure.feature("Shop By Category")
@pytest.mark.parametrize(
    "data",
    CSVReader.read_csv("shop_by_category_data.csv")
)
@pytest.mark.order(2)
def test_shop_by_category_data(driver, data):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    category_name = data["category_name"]
    expected_result = data["expected_result"]

    if expected_result == "visible":

        actual_result = shop_by_category_page.is_category_visible(
            category_name,
            timeout=5
        )

        assert actual_result is True, \
            f"{category_name} category should be visible"

    elif expected_result == "not_visible":

        actual_result = shop_by_category_page.is_category_visible(
            category_name,
            timeout=2
        )

        assert actual_result is False, \
            f"{category_name} category should not be visible"


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