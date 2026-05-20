import pytest

from pages.loginpage import LoginPage
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