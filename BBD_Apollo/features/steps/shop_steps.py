from behave import when, then

from pages.shop_by_category_page import ShopByCategoryPage


@then('category "{category_name}" should be "{expected_result}"')
def step_validate_category(context, category_name, expected_result):

    shop_page = ShopByCategoryPage(context.driver)

    if expected_result == "visible":

        actual_result = shop_page.is_category_visible(
            category_name,
            timeout=5
        )

        assert actual_result is True, \
            f"{category_name} category should be visible"

    elif expected_result == "not_visible":

        actual_result = shop_page.is_category_visible(
            category_name,
            timeout=2
        )

        assert actual_result is False, \
            f"{category_name} category should not be visible"


@when("user opens Health Monitors category")
def step_open_health_monitors(context):

    shop_page = ShopByCategoryPage(context.driver)

    context.shop_page = shop_page

    shop_page.click_health_monitors()


@then("Health Monitors page should be opened")
def step_health_monitors_opened(context):

    shop_page = getattr(
        context,
        "shop_page",
        ShopByCategoryPage(context.driver)
    )

    assert shop_page.is_health_monitors_page_opened(), \
        "Health Monitors page did not open"


@then("Brands filter should be visible")
def step_brands_filter_visible(context):

    assert context.shop_page.is_brands_filter_visible(), \
        "Brands filter is not visible"


@when("user applies Doctor S Choice filter")
def step_apply_doctor_filter(context):

    context.shop_page.apply_doctor_s_choice_filter()


@when("user adds Doctor S Choice product to cart")
def step_add_product_to_cart(context):

    shop_page = ShopByCategoryPage(context.driver)

    context.shop_page = shop_page

    context.product_name = (
        shop_page.add_exact_product_to_cart_with_retry(
            max_attempts=3
        )
    )

    assert context.product_name is not None, \
        "Product name was not captured"


@then("cart page should be opened")
def step_cart_page_opened(context):

    assert context.shop_page.is_cart_page_opened(), \
        "Cart page did not open"


@then("selected product should be present in cart")
def step_product_present_in_cart(context):

    assert context.shop_page.is_exact_product_present_in_cart(
        context.product_name
    ), f"Expected product not found in cart: {context.product_name}"


@when("user clicks Proceed button")
def step_click_proceed(context):

    context.shop_page.click_proceed_button()


@then("next cart step should be opened")
def step_next_cart_step_opened(context):

    assert context.shop_page.is_after_proceed_page_opened(), \
        "Page did not move forward after clicking Proceed"