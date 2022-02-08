import pandas as pd
import numpy as np
import re
from handlers.users.parser.parser import FlatInfoSoup
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

try:
    df = pd.read_csv('DataFrameFlat.csv')
except:
    df = pd.DataFrame()


def house_preobras(house):
    """
    Чистка номера дома от мусора
    """
    house_list = list(house)

    for i in range(len(house_list)):

            if house_list[i] == 'с' or house_list[i] == 'С' or house_list[i] == 'к' or house_list[i] == 'К':
                house_list.pop(i)

                for j in range(i, len(house_list)):
                    house_list.pop(i)
                break

    house = ''.join(house_list)

    return house

def df_append(soup):
    """
    Добавляем информацию в фрейм
    """

    global df
    fio = FlatInfoSoup()
    flat_dict = {}
    flat_dict['flat_name'] = fio.name(soup)
    flat_dict['price'] = fio.price(soup)

    try:
        flat_dict['city'] = fio.mesto(soup)[0]

    except IndexError:
        flat_dict['city'] = 'NaN'


    try:
        flat_dict['okrug'] = fio.mesto(soup)[1]

    except IndexError:
        flat_dict['okrug'] = 'NaN'


    try:
        flat_dict['district'] = fio.mesto(soup)[2]

    except IndexError:
        flat_dict['district'] = 'NaN'


    try:
        flat_dict['street'] = fio.mesto(soup)[3]

    except IndexError:
        flat_dict['street'] = 'NaN'


    try:
        flat_dict['house'] = fio.mesto(soup)[4]

    except IndexError:
        flat_dict['house'] = 'NaN'


    flat_dict['metro_time'] = round(np.mean(fio.metro_time(soup)),2)


    for i in range(len(fio.res_info(soup))):
        flat_dict[fio.res_info(soup)[i].findAll('span', attrs= {'class':'a10a3f92e9--name--x7_lt'})[0].text] = fio.res_info(soup)[i].findAll('span', attrs= {'class':'a10a3f92e9--value--Y34zN'})[0].text


    for i in range(len(fio.house_info(soup))):
        flat_dict[fio.house_info(soup)[i].findAll('div', attrs= {'class':'a10a3f92e9--name--pLPu9'})[0].text] = fio.house_info(soup)[i].findAll('div', attrs= {'class':'a10a3f92e9--value--G2JlN'})[0].text


    for i in range(len(fio.square_floor(soup))):
        flat_dict[fio.square_floor(soup)[i].findAll('div', attrs = {'class': 'a10a3f92e9--info-title--JWtIm'})[0].text] = fio.square_floor(soup)[i].findAll('div', attrs = {'class': 'a10a3f92e9--info-value--bm3DC'})[0].text.replace('\xa0', ' ')


    try:
        flat_dict['Залог'] = re.findall(r'\d+', fio.price_info(soup)[0])[0]

    except IndexError:
        flat_dict['Залог'] = 0


    try:
        flat_dict['Комиссия'] = re.findall(r'\d+', fio.price_info(soup)[1])[0]

    except IndexError:
        flat_dict['Комиссия'] = 0


    try:
        flat_dict['Предоплата'] = re.findall(r'\d+', fio.price_info(soup)[2])[0]

    except IndexError:
        flat_dict['Предоплата'] = 0
        
        
    try: 
        flat_dict['Холодильник'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--fridge--MD46C'})[0].text

    except IndexError:
        flat_dict['Холодильник'] = 0

    if flat_dict['Холодильник'] != 0:
        flat_dict['Холодильник'] = 1
        
        
    try: 
        flat_dict['Посудомоечная машина'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--dishwasher--gOo3q'})[0].text

    except IndexError:
        flat_dict['Посудомоечная машина'] = 0

    if flat_dict['Посудомоечная машина'] != 0:
        flat_dict['Посудомоечная машина'] = 1
    

    try: 
        flat_dict['Стиральная машина'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--washing--qc1qA'})[0].text

    except IndexError:
        flat_dict['Стиральная машина'] = 0

    if flat_dict['Стиральная машина'] != 0:
        flat_dict['Стиральная машина'] = 1


    try: 
        flat_dict['Мебель в комнатах'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--furniture--Sr1eM'})[0].text
    except IndexError:

        flat_dict['Мебель в комнатах'] = 0

    if flat_dict['Мебель в комнатах'] != 0:
        flat_dict['Мебель в комнатах'] = 1


    try: 
        flat_dict['Мебель на кухне'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--kitchen--vWMSE'})[0].text

    except IndexError:
        flat_dict['Мебель на кухне'] = 0

    if flat_dict['Мебель на кухне'] != 0:
        flat_dict['Мебель на кухне'] = 1


    try: 
        flat_dict['Кондиционер'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--cond--aoNs9'})[0].text

    except IndexError:
        flat_dict['Кондиционер'] = 0

    if flat_dict['Кондиционер'] != 0:
        flat_dict['Кондиционер'] = 1


    try: 
        flat_dict['Телевизор'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--tv--pjPm3'})[0].text

    except IndexError:
        flat_dict['Телевизор'] = 0

    if flat_dict['Телевизор'] != 0:
        flat_dict['Телевизор'] = 1


    try: 
        flat_dict['Интернет'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--internet--y7V4t'})[0].text

    except IndexError:
        flat_dict['Интернет'] = 0

    if flat_dict['Интернет'] != 0:
        flat_dict['Интернет'] = 1


    try: 
        flat_dict['Ванна'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--bath--T6AIO'})[0].text

    except IndexError:
        flat_dict['Ванна'] = 0

    if flat_dict['Ванна'] != 0:
        flat_dict['Ванна'] = 1


    try: 
        flat_dict['Душевая кабина'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--CqUH9 a10a3f92e9--shower--zGoTh'})[0].text

    except IndexError:
        flat_dict['Душевая кабина'] = 0

    if flat_dict['Душевая кабина'] != 0:
        flat_dict['Душевая кабина'] = 1


    geocoder = RateLimiter(Nominatim(user_agent='tutorial').geocode, min_delay_seconds=1)
    dictionary = geocoder('Москва, {}'.format(str(flat_dict['street']) + ' ' + str(house_preobras(flat_dict['house'])))).raw
    flat_dict['coord'] = ' '.join([dictionary['lat'], dictionary['lon']])
    flat_dict['lat'] = float(dictionary['lat'])
    flat_dict['lon'] = float(dictionary['lon'])

    df = df.append(flat_dict, ignore_index = True)

    return df

