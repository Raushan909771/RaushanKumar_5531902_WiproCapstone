from selenium.webdriver.common.by import By


class ShopLocators:

    HEALTH_MONITORS_TEXT = (
        By.XPATH,
        "//*[normalize-space()='Health Monitors']"
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