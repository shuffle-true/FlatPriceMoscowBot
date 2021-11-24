from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
from geopy import distance
from collections import OrderedDict
import operator




def chrome_open_server():
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    chrome=webdriver.Chrome(options=options)
    return chrome

def pages_count_server(minprice, maxprice):

    page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p=1&region=1&type=4'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    chrome=webdriver.Chrome(options=options)
    chrome.get(page_link)
    soup = BeautifulSoup(chrome.page_source, features = 'html.parser')
    return soup

def links_flat_server(maxprice, minprice, answer_count_page):
    df_flat_links = pd.DataFrame()
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    chrome=webdriver.Chrome(options=options)

    for i in range(1, int(answer_count_page)):
        page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p={i}&region=1&type=4'
        chrome.get(page_link)
        soup = BeautifulSoup(chrome.page_source, features="html.parser")
        flat_links = soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['_93444fe79c--link--39cNw'])
        flat_list = [link.attrs['href'] for link in flat_links]
        for i in range(len(flat_list)):
            df_flat_links = df_flat_links.append({'links': flat_list[i]}, ignore_index = True)
        return df_flat_links

def dist_metro_server(house_coord):
    df_metro = pd.read_csv('/home/ubuntu/FlatPriceMoscowBot/METRO.csv')
    dist_metro = {}
    for i in range(df_metro.shape[0]):
        dist_metro[df_metro['station_name'][i]] = round(distance.distance(df_metro['coord'][i], house_coord).km,
                                                        2)
    sorted_dist_metro_tuple = sorted(dist_metro.items(), key = operator.itemgetter(1))
    sorted_dist_metro_dict = OrderedDict()
    for k, v in sorted_dist_metro_tuple:
        sorted_dist_metro_dict[k] = v
    keys_list = list(sorted_dist_metro_dict.keys())
    return keys_list, sorted_dist_metro_dict


def get_flat_server(flat_links, i):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument('--no-sandbox')
    options.add_argument("--disable-setuid-sandbox")
    chrome=webdriver.Chrome(options=options)
    chrome.get(flat_links[int(i)])
    soup = BeautifulSoup(chrome.page_source, features="html.parser")
    return soup