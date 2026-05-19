import pytest

from pages.shopbycategorypage import ShopByCategoryPage
from utils.csv_reader import CSVReader
from utils.config_reader import ConfigReader


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


@pytest.mark.order(3)
def test_click_health_monitors_category(driver):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    shop_by_category_page.click_health_monitors()

    assert shop_by_category_page.is_health_monitors_page_opened(), \
        "Health Monitors page did not open"


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


@pytest.mark.order(5)
def test_add_doctor_s_choice_product_to_cart(driver):

    driver.get(ConfigReader.get("base_url"))

    shop_by_category_page = ShopByCategoryPage(driver)

    shop_by_category_page.click_health_monitors()

    assert shop_by_category_page.is_health_monitors_page_opened(), \
        "Health Monitors page did not open"

    shop_by_category_page.apply_doctor_s_choice_filter()

    product_name = shop_by_category_page.add_one_doctor_s_choice_product_to_cart()

    shop_by_category_page.go_to_cart()

    assert shop_by_category_page.is_cart_page_opened(), \
        "Cart page did not open after adding product"

    assert shop_by_category_page.is_exact_product_present_in_cart(product_name), \
        f"Expected product not found in cart: {product_name}"