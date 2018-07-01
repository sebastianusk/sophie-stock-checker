from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox(firefox_binary=FirefoxBinary())

URL_CHECKOUT_CART = "https://www.sophieparis.com/checkout/cart/"
productCode = "T3246B5"
numberOfItems = 100

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
numberOfItemsField.send_keys(str(numberOfItems))

# click button
confirmButton = driver.find_element_by_id(
    'btnSubmitFastAddToCart').find_element_by_class_name('button')
confirmButton.click()

messages = WebDriverWait(driver,   5).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'messages'))
)
try:
    messages.find_element_by_class_name('success-msg')
    driver.delete_all_cookies()
    driver.get(URL_CHECKOUT_CART)
except Exception as e:
    print(e)
    complete = 'failed'
