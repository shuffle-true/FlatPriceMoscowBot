from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from data.all_config import Andrew_PATH_driver
import pandas as pd
from handlers.users.logic.config_for_server import chrome_open_server, pages_count_server, links_flat_server, get_flat_server
import re

def chrome_open():
    """
    
    Запускаем Хром

    """
    try:
        chrome = chrome_open_server()
    except:
        chrome = webdriver.Chrome(Andrew_PATH_driver)
        chrome.minimize_window()
    return chrome
    
def pages_count(minprice, maxprice):

    page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p=1&region=1&type=4'

    try:
        chrome = pages_count_server()
    except:
        chrome = webdriver.Chrome(Andrew_PATH_driver)
        chrome.minimize_window()
        chrome.get(page_link)

    soup = BeautifulSoup(chrome.page_source, features="html.parser")
    return soup

def links_flat(maxprice, minprice, answer_count_page):
    try:
        df_flat_links = links_flat_server(maxprice, minprice, answer_count_page)
    except:
        df_flat_links = pd.DataFrame()
        chrome = webdriver.Chrome(Andrew_PATH_driver)
        chrome.minimize_window()
        for i in range(1, int(answer_count_page)):
            page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p={i}&region=1&type=4'
            chrome.get(page_link)
            soup = BeautifulSoup(chrome.page_source, features="html.parser")
            flat_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['_93444fe79c--link--39cNw'])
            flat_list = [link.attrs['href'] for link in flat_links]
            for i in range(len(flat_list)):
                df_flat_links = df_flat_links.append({'links': flat_list[i]}, ignore_index = True)
    return df_flat_links

def get_flat(flat_links, i):
    try:
        soup = get_flat_server(flat_links, i)
    except:
        chrome = webdriver.Chrome(Andrew_PATH_driver)
        chrome.minimize_window()
        chrome.get(flat_links[int(i)])
        soup = BeautifulSoup(chrome.page_source, features="html.parser")
    return soup

def name(soup):
    name = soup.find('h1', attrs= {'class':'a10a3f92e9--title--2Widg'}).text
    return name
def price(soup):
    price = soup.findAll('span', attrs= {'class':'a10a3f92e9--price_value--1iPpd'})[0].text.replace('\xa0', ' ').replace('₽/мес.', '').strip()
    return price

def metro_time(soup):
    metro_time_list = []
    metro_time = soup.findAll('span', attrs= {'class':'a10a3f92e9--underground_time--1fKft'})
    for i in range(len(metro_time)):
        metro_time_list.append(int(re.findall(r'\d+', metro_time[i].text)[0]))
    return metro_time_list

def mesto(soup):
    mesto_list = []
    mesto = soup.findAll('a', attrs= {'class':'a10a3f92e9--link--1t8n1 a10a3f92e9--address-item--1clHr'})
    for i in range (len(mesto)):
        mesto_list.append(mesto[i].text)
    return mesto_list

def price_info(soup):
    price_info = soup.findAll('p', attrs= {'class':'a10a3f92e9--description--2xRVn'})
    price_info = price_info[0].text.replace('\xa0', "").split(',')
    return price_info[0:3]

def square_floor(soup):
    square_floor = soup.findAll('div', attrs = {'class': 'a10a3f92e9--info--3NBVV'})
    return square_floor

def res_info(soup):
    res_info = soup.findAll('li', attrs= {'class':'a10a3f92e9--item--_ipjK'})
    return res_info

def house_info(soup):
    house_info = soup.findAll('div', attrs= {'class':'a10a3f92e9--item--2Ig2y'})
    return house_info