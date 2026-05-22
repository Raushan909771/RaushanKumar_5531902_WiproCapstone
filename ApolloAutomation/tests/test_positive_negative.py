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