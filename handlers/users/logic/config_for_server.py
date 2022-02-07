"""
Конфигурация для работы парсера на удаленном сервере

"""

from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from geopy import distance
from collections import OrderedDict
import operator
from typing import List, Dict



class ParserServer:
    """
    Класс парсера, при запуске с сервера
    """
    def __init__(self) -> None:
        """
        Класс отвечает за парсинг квартир при запуске с сервера

        Необходим предустановленный Chrome (нужную версию Chrome см. в документации)
        """
        pass

    def chrome_open_server(self):
        """
        Тестовый запуск хрома
        """

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-setuid-sandbox")

        self.chrome=webdriver.Chrome(options=self.options)

        return self.chrome

    def pages_count_server(self, minprice: int, maxprice: int) -> BeautifulSoup:
        """
        Собирает информацию о кол-ве страниц, найденных в определенном ценовом диапазоне

        Paramets:
        ----------------
        minprice: str - начальный диапазон цены
        maxprice: str - конечный диапазон цены

        Return:
        ----------------
        self.soup: BeautifulSoup - HTML код страницы, в котором заложены ссылки на квартиры

        Example:
        ----------------
        >>> ParserServer().pages_count_server(100000, 150000)
        >>> "soup"

        """

        self.page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p=1&region=1&type=4'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-setuid-sandbox")
        self.chrome=webdriver.Chrome(options=self.options)
        self.chrome.get(self.page_link)
        self.soup = BeautifulSoup(self.chrome.page_source, features = 'html.parser')

        return self.soup

    def links_flat_server(self, maxprice: int, minprice: int, answer_count_page: int) -> pd.DataFrame:
        """
        Формирование фрейма с ссылками на квартиры

        Paramets:
        ----------------
        minprice: str - начальный диапазон цены
        maxprice: str - конечный диапазон цены
        answer_count_page: int - до какой страницы парсить квартиры (не превышает 54)

        Return:
        ----------------
        self.df_flat_links: pd.DataFrame - фрейм, содержащий ссылки на квартиры

        Example:
        ----------------
        >>> ParserServer().links_flat_server(100000, 150000, 20)
        >>> pd.DataFrame

        """

        self.df_flat_links = pd.DataFrame()

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-setuid-sandbox")

        self.chrome=webdriver.Chrome(options=self.options)

        for i in range(1, int(answer_count_page)):
            self.page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}&minprice={minprice}&offer_type=flat&p={i}&region=1&type=4'
            self.chrome.get(self.page_link)
            self.soup = BeautifulSoup(self.chrome.page_source, features="html.parser")

            self.flat_links = self.soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['_93444fe79c--link--39cNw'])
            self.flat_list = [link.attrs['href'] for link in self.flat_links]

            for i in range(len(self.flat_list)):
                self.df_flat_links = self.df_flat_links.append({'links': self.flat_list[i]}, ignore_index = True)

            return self.df_flat_links

    def dist_metro_server(self, house_coord: str) -> [List[str], Dict]:
        """
        Подсчет расстояния до метро

        Paramets:
        ----------------
        house_coord: str - координаты дома

        Return:
        ----------------
        self.keys_list: List[str] - список отсортированных названий станций (ключи к словарю),
        self.sorted_dist_metro_dict: Dict - отсортированный по расстоянию словарь.
        Ключ - название станции, значение - расстояние до станции

        Example:
        ----------------
        >>> ParserServer().dist_metro_server('58.989821 38.121234')

        """

        self.df_metro = pd.read_csv('/home/ubuntu/FlatPriceMoscowBot/METRO.csv')
        self.dist_metro = {}

        for i in range(self.df_metro.shape[0]):
            self.dist_metro[self.df_metro['station_name'][i]] = round(distance.distance(self.df_metro['coord'][i], house_coord).km,
                                                            2)

        self.sorted_dist_metro_tuple = sorted(self.dist_metro.items(), key = operator.itemgetter(1))
        self.sorted_dist_metro_dict = OrderedDict()

        for k, v in self.sorted_dist_metro_tuple:
            self.sorted_dist_metro_dict[k] = v

        self.keys_list = list(self.sorted_dist_metro_dict.keys())

        return self.keys_list, self.sorted_dist_metro_dict


    def get_flat_server(self, flat_links: str, i: int) -> BeautifulSoup:
        """
        Парсинг конкретной квартиры

        Paramets:
        ----------------
        flat_links: str - ссылка на квартиру из фрейма, полученного в методе links_flat_server()
        i: int - счетчик цикла

        Return:
        ----------------
        self.soup: BeautifulSoup - HTML код квартиры

        Example:
        ----------------
        >>> ParserServer().get_flat_server('cian.com/125746794', 2)
        >>> self.soup

        """

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument("--disable-setuid-sandbox")

        self.chrome=webdriver.Chrome(options=self.options)
        self.chrome.get(flat_links[int(i)])

        self.soup = BeautifulSoup(self.chrome.page_source, features="html.parser")
        return self.soup