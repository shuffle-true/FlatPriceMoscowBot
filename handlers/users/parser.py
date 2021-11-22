from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import time

def chrome_open():
    """
    
    Запускаем Хром
    """
    chrome = webdriver.Chrome(r'C:\Users\Sveta\PycharmProjects\FlatPriceMoscowBot\handlers\users\chromedriver.exe')
    return chrome
    
