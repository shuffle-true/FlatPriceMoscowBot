from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from data.all_config import Andrew_PATH_driver
import time

def chrome_open():
    """
    
    Запускаем Хром
    """
    chrome = webdriver.Chrome(Andrew_PATH_driver)
    return chrome
    
def pages_count(minprice, maxprice):

    page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p=1&region=1&type=4'

    chrome = webdriver.Chrome(Andrew_PATH_driver)
    chrome.minimize_window()
    chrome.get(page_link)

    soup = BeautifulSoup(chrome.page_source, features="html.parser")

    return soup

def links_flat(maxprice, minprice, answer_count_page):
    chrome = webdriver.Chrome(Andrew_PATH_driver)
    chrome.minimize_window()
    flat_list = []
    for i in range(1, int(answer_count_page)):
        page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p={i}&region=1&type=4'
        chrome.get(page_link)
        soup = BeautifulSoup(chrome.page_source, features="html.parser")
        flat_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['_93444fe79c--link--39cNw'])
        flat_links = [link.attrs['href'] for link in flat_links]
        flat_list.append(flat_links)
    return flat_list