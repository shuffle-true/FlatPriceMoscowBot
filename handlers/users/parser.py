from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time

def chrome_open():
    chrome = webdriver.Chrome(r'C:\Users\Andrew\Documents\Develop VS Code\Telegram Bot\Flat Price Moscow\handlers\users\chromedriver.exe')
    time.sleep(10)