from selenium import webdriver
from bs4 import BeautifulSoup
from data.all_config import Andrew_PATH_driver
import pandas as pd
import warnings
warnings.filterwarnings('ignore')
import re


class Parser:
    """

    Класс парсинга информации о квартире

    """

    def __init__(self):
        pass

    def chrome_open(self):
        """
        Тестовый запуск хрома
        """

        self.__chrome = webdriver.Chrome(service = Andrew_PATH_driver)
        self.__chrome.minimize_window()

        self.__chrome.close()

        return


    def pages_count(self, minprice: int, maxprice: int):
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
         >>> Parser().pages_count(100000, 150000)
         >>> "soup"
        """

        self.__chrome = webdriver.Chrome(service = Andrew_PATH_driver)
        self.__chrome.minimize_window()

        self.page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}' \
                         f'&minprice={minprice}&offer_type=flat&p=1&region=1&type=4'

        self.__chrome.get(self.page_link)

        self.soup = BeautifulSoup(self.__chrome.page_source, features="html.parser")

        self.__chrome.close()

        return self.soup



    def links_flat(self, maxprice: int, minprice: int, answer_count_page: int):
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

        self._df_flat_links = pd.DataFrame()

        self.__chrome = webdriver.Chrome(service = Andrew_PATH_driver)
        self.__chrome.minimize_window()


        for i in range(1, int(answer_count_page)):
            page_link = f'https://www.cian.ru/cat.php?currency=2&deal_type=rent&engine_version=2&maxprice={maxprice}' \
                        f'&minprice={minprice}&offer_type=flat&p={i}&region=1&type=4'

            self.__chrome.get(page_link)

            self.soup = BeautifulSoup(self.__chrome.page_source, features="html.parser")

            self.flat_links = self.soup.findAll(lambda tag: tag.name == 'a' and tag.get('class') == ['_93444fe79c--link--eoxce'])
            self.flat_list = [link.attrs['href'] for link in self.flat_links]


            for i in range(len(self.flat_list)):
                self._df_flat_links = self._df_flat_links.append({'links': self.flat_list[i]}, ignore_index = True)

        self.__chrome.close()

        return self._df_flat_links

    def get_flat(self, flat_links: pd.DataFrame, i: int):
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

        self.__options = webdriver.ChromeOptions()
        self.__options.add_argument('headless')
        self.__options.add_argument('--no-sandbox')
        self.__options.add_argument("--disable-setuid-sandbox")

        self.__chrome = webdriver.Chrome(service = Andrew_PATH_driver, options=self.__options)
        self.__chrome.minimize_window()

        self.__chrome.get(flat_links[int(i)])
        self.soup = BeautifulSoup(self.__chrome.page_source, features="html.parser")

        self.__chrome.close()

        return self.soup




class FlatInfoSoup:
    """

    В этом классе собираем информацию о квартире

    """

    def __init__(self):
        pass


    def name(self, soup):
        """
        Имя объявления
        """

        self.__name = soup.find('h1', attrs={'class': 'a10a3f92e9--title--UEAG3'}).text

        return self.__name



    def price(self, soup):
        """
        Аренда
        """

        self.__price = soup.findAll('span', attrs= {'class':'a10a3f92e9--price_value--lqIK0'})[0].text.replace('\xa0', ' ').replace('₽/мес.', '').strip()

        return self.__price



    def metro_time(self, soup):
        """
        Время до метро
        """

        self.__metro_time_list = []
        self.__metro_time = soup.findAll('span', attrs= {'class':'a10a3f92e9--underground_time--iOoHy'})

        for i in range(len(self.__metro_time)):
            self.__metro_time_list.append(int(re.findall(r'\d+', self.__metro_time[i].text)[0]))

        return self.__metro_time_list



    def mesto(self, soup):
        """
        Информация о районе округе и тд
        """

        self.__mesto_list = []
        self.__mesto = soup.findAll('a', attrs= {'class':'a10a3f92e9--link--ulbh5 a10a3f92e9--address-item--ScpSN'})

        for i in range (len(self.__mesto)):
            self.__mesto_list.append(self.__mesto[i].text)

        return self.__mesto_list



    def price_info(self, soup):
        """
        Залог, предоплата, коммисия
        """

        self.__price_info = soup.findAll('p', attrs= {'class':'a10a3f92e9--description--CPyUa'})
        self.__price_info = self.__price_info[0].text.replace('\xa0', "").split(',')

        return self.__price_info[0:3]



    def square_floor(self, soup):
        """
        Площадь, этаж
        """

        self.__square_floor = soup.findAll('div', attrs = {'class': 'a10a3f92e9--info--PZznE'})

        return self.__square_floor



    def res_info(self, soup):
        """
        Наличие фурнитуры, ванная комната и т.д.
        """

        self.__res_info = soup.findAll('ul', attrs= {'class':'a10a3f92e9--item--d9uzC'})

        return self.__res_info

    def house_info(self, soup):
        """
        Информация о доме (год постройки, материал, парковка и т.д)
        """

        self.__house_info = soup.findAll('div', attrs= {'class':'a10a3f92e9--item--M4jGb'})

        return self.__house_info