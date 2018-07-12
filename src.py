
#!/usr/bin/python3

from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys


driver = webdriver.Chrome()

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
    productCodeField.send_keys(Keys.TAB)
    driver.implicitly_wait(1)
    # input number of items
    numberOfItemsField = driver.find_element_by_id('fastAddQty')
    numberOfItemsField.clear()
    numberOfItemsField.send_keys(str(amount))
    driver.implicitly_wait(1)
    # click button
    confirmButton = driver.find_element_by_id(
        'btnSubmitFastAddToCart').find_element_by_class_name('button')
    confirmButton.click()
    driver.implicitly_wait(1)
    try:
        driver.find_element_by_class_name('messages')
    except Exception:
        checkProduct(productCode, amount)

    try:
        driver.find_element_by_class_name('page-title')
        return True
    except Exception:
        return False


def checkRecursively(productCode, min, max):
    mid = (max + min) // 2
    try:
        check = checkProduct(productCode, mid)
    except Exception as e:
        return 0
    if min == mid:
        return min
    if check:
        return checkRecursively(productCode, mid, max)
    else:
        return checkRecursively(productCode, min, mid)


OUTPUT_FILE = "output.txt"

if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

with open('input.txt') as f:
    lines = f.readlines()
    for line in lines:
        result = checkRecursively(line.rstrip(), 0, 9999)
        print(line.rstrip(), result)
        with open(OUTPUT_FILE, "a+") as file:
            file.write(f'{line.rstrip()}\tamount: {result} \n')


driver.close()
