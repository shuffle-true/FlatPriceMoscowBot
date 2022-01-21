import pandas as pd
import numpy as np
import re
from handlers.users.parser.parser import name, price, metro_time, mesto, price_info, square_floor, res_info, house_info
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

try:
    df = pd.read_csv('DataFrameFlat.csv')
except:
    df = pd.DataFrame()


def house_preobras(house):
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
    global df
    flat_dict = {}
    flat_dict['flat_name'] = name(soup)
    flat_dict['price'] = price(soup)
    try:
        flat_dict['city'] = mesto(soup)[0]
    except IndexError:
        flat_dict['city'] = 'NaN'
    
    try:
        flat_dict['okrug'] = mesto(soup)[1]
    except IndexError:
        flat_dict['okrug'] = 'NaN'
        
    try:
        flat_dict['district'] = mesto(soup)[2]
    except IndexError:
        flat_dict['district'] = 'NaN'
        
    try:
        flat_dict['street'] = mesto(soup)[3]
    except IndexError:
        flat_dict['street'] = 'NaN'
    
    try:
        flat_dict['house'] = mesto(soup)[4]
    except IndexError:
        flat_dict['house'] = 'NaN'

    flat_dict['metro_time'] = round(np.mean(metro_time(soup)),2)

    for i in range(len(res_info(soup))):
        flat_dict[res_info(soup)[i].findAll('span', attrs= {'class':'a10a3f92e9--name--3bt8k'})[0].text] = res_info(soup)[i].findAll('span', attrs= {'class':'a10a3f92e9--value--3Ftu5'})[0].text
            
    for i in range(len(house_info(soup))):
        flat_dict[house_info(soup)[i].findAll('div', attrs= {'class':'a10a3f92e9--name--22FM0'})[0].text] = house_info(soup)[i].findAll('div', attrs= {'class':'a10a3f92e9--value--38caj'})[0].text

    for i in range(len(square_floor(soup))):
        flat_dict[square_floor(soup)[i].findAll('div', attrs = {'class': 'a10a3f92e9--info-title--9Jq07'})[0].text] = square_floor(soup)[i].findAll('div', attrs = {'class': 'a10a3f92e9--info-value--3Nvt6'})[0].text.replace('\xa0', ' ')    

    try:
        flat_dict['Залог'] = re.findall(r'\d+', price_info(soup)[0])[0]
    except IndexError:
        flat_dict['Залог'] = 0
        
    try:
        flat_dict['Комиссия'] = re.findall(r'\d+', price_info(soup)[1])[0]
    except IndexError:
        flat_dict['Комиссия'] = 0
        
    try:
        flat_dict['Предоплата'] = re.findall(r'\d+', price_info(soup)[2])[0]
    except IndexError:
        flat_dict['Предоплата'] = 0
        
        
    try: 
        flat_dict['Холодильник'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--fridge--3dT0J'})[0].text
    except IndexError:
        flat_dict['Холодильник'] = 0
    if flat_dict['Холодильник'] != 0:
        flat_dict['Холодильник'] = 1
        
        
    try: 
        flat_dict['Посудомоечная машина'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--dishwasher--2Jedr'})[0].text
    except IndexError:
        flat_dict['Посудомоечная машина'] = 0
    if flat_dict['Посудомоечная машина'] != 0:
        flat_dict['Посудомоечная машина'] = 1
    
    
    
    try: 
        flat_dict['Стиральная машина'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--washing--FcpyQ'})[0].text
    except IndexError:
        flat_dict['Стиральная машина'] = 0
    if flat_dict['Стиральная машина'] != 0:
        flat_dict['Стиральная машина'] = 1



    try: 
        flat_dict['Мебель в комнатах'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--furniture--35Zny'})[0].text
    except IndexError:
        flat_dict['Мебель в комнатах'] = 0
    if flat_dict['Мебель в комнатах'] != 0:
        flat_dict['Мебель в комнатах'] = 1



    try: 
        flat_dict['Мебель на кухне'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--kitchen--3nY3i'})[0].text
    except IndexError:
        flat_dict['Мебель на кухне'] = 0
    if flat_dict['Мебель на кухне'] != 0:
        flat_dict['Мебель на кухне'] = 1




    try: 
        flat_dict['Кондиционер'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--cond--3WZYH'})[0].text
    except IndexError:
        flat_dict['Кондиционер'] = 0
    if flat_dict['Кондиционер'] != 0:
        flat_dict['Кондиционер'] = 1




    try: 
        flat_dict['Телевизор'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--tv--1JNtB'})[0].text
    except IndexError:
        flat_dict['Телевизор'] = 0
    if flat_dict['Телевизор'] != 0:
        flat_dict['Телевизор'] = 1


    try: 
        flat_dict['Интернет'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--internet--nlRGv'})[0].text
    except IndexError:
        flat_dict['Интернет'] = 0
    if flat_dict['Интернет'] != 0:
        flat_dict['Интернет'] = 1



    try: 
        flat_dict['Ванна'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--bath--Zx2LA'})[0].text
    except IndexError:
        flat_dict['Ванна'] = 0
    if flat_dict['Ванна'] != 0:
        flat_dict['Ванна'] = 1



    try: 
        flat_dict['Душевая кабина'] = soup.findAll('li', attrs = {'class': 'a10a3f92e9--item--Ecr_d a10a3f92e9--shower--2jBm5'})[0].text
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
