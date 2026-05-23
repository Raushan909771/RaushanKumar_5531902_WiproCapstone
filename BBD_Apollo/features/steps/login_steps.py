from behave import given, when, then

from pages.login_page import LoginPage
from utils.config_reader import ConfigReader


@given("user opens Apollo application")
def step_open_application(context):

    context.driver.get(ConfigReader.get_base_url())


@when("user enters valid mobile number")
def step_enter_mobile_number(context):

    login_page = LoginPage(context.driver)

    context.login_page = login_page

    login_page.login_with_mobile_number(
        ConfigReader.get("mobile_number")
    )


@then("OTP screen should be visible")
def step_otp_screen_visible(context):

    assert context.login_page.is_otp_screen_visible(), \
        "OTP screen should be visible after entering mobile number"


@when("user enters OTP manually")
def step_enter_otp_manually(context):

    print("\nEnter OTP manually in browser.")
    print("Do not press anything in terminal.")
    print("Automation will continue automatically after OTP is entered.")
    print("Maximum wait time is 60 seconds.\n")

    context.otp_submitted = (
        context.login_page.wait_for_otp_entry_and_submit(
            timeout=60
        )
    )


@then("login should be submitted successfully")
def step_login_submitted(context):

    assert context.otp_submitted is True, \
        "OTP was not entered or submitted successfully"