from selenium import webdriver
import os
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

driver = webdriver.Firefox(firefox_binary=FirefoxBinary())

def addItem(productCode, quantity):
    URL_ADD = 'https://www.sophieparis.com/fastadd/index/addtocart'
    return requests.post(
        URL_ADD,
        data={
            'sku': productCode,
            'qty': quantity,
            'product_id': ''
        }
    ).json()['url']


def openUrl(url):
    return driver.get(url).content


def getSoup(content):
    return BeautifulSoup(content, 'html.parser').prettify


def removeIfExist(fileName):
    if os.path.exists(fileName):
        os.remove(fileName)


def writeToFile(text):
    fileName = "source.html"
    removeIfExist(fileName)
    file = open(fileName, "w")
    file.write(str(text))
    file.close()


responseAdd = addItem('T3246B5', 100)

if responseAdd:
    writeToFile(getSoup(openUrl(responseAdd)))
else:
    print('product not found')
