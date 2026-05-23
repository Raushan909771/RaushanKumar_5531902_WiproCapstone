from selenium.webdriver.common.by import By


class LoginLocators:

    LOGIN_ICON = (
        By.XPATH,
        "//*[contains(text(),'Login') or contains(text(),'Sign in') or contains(text(),'Sign In')]"
    )

    MOBILE_INPUT = (
        By.XPATH,
        "//input"
    )

    CONTINUE_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Continue')]"
    )

    OTP_SCREEN_TEXT = (
        By.XPATH,
        "//*[contains(text(),'OTP') or contains(text(),'otp') or contains(text(),'Resend') or contains(text(),'sent')]"
    )

    VERIFY_BUTTON = (
        By.XPATH,
        "//button[contains(text(),'Verify') or contains(text(),'Continue') or contains(text(),'Submit')]"
    )