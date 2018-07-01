from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(firefox_binary=FirefoxBinary())

URL_CHECKOUT_CART = "https://www.sophieparis.com/checkout/cart/"


def checkProduct(productCode, amount):
    driver.delete_all_cookies()
    driver.get(URL_CHECKOUT_CART)

    # close dialog
    closeButton = WebDriverWait(driver,     5).until(
        EC.presence_of_element_located((By.CLASS_NAME, "fancybox-close")))
    closeButton.click()

    WebDriverWait(driver,   5).until_not(
        EC.presence_of_element_located((By.CLASS_NAME, 'fancybox-overlay')))

    # input product code
    productCodeField = driver.find_element_by_id('productReference')
    productCodeField.send_keys(productCode)
    autoComplete = driver.find_element_by_class_name('autocomplete-suggestion')
    autoComplete.click()

    # input number of items
    numberOfItemsField = driver.find_element_by_id('fastAddQty')
    numberOfItemsField.send_keys(str(amount))

    # click button
    confirmButton = driver.find_element_by_id(
        'btnSubmitFastAddToCart').find_element_by_class_name('button')
    confirmButton.click()

    try:
        driver.find_element_by_class_name('page-title')
        return True
    except Exception:
        return False


def checkRecursively(productCode, min, max):
    mid = (max + min) // 2
    check = checkProduct(productCode, mid)
    print(f'min: {min}, mid: {mid}, max: {max}, check: {check}')
    if min == mid:
        return min
    if check:
        return checkRecursively(productCode, mid, max)
    else:
        return checkRecursively(productCode, min, mid)


result = checkRecursively("T3246B5", 0, 9999)
print(result)
