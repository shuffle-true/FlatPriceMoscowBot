from aiogram import types
import operator
import statistics as st
from keyboards.default import menu_first
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp
from states import MenuButton
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context
from collections import OrderedDict

## Кремлевские координаты
coord_kreml = '55.751999 37.617734'
dict_df_hard = {}


def adress_preobras(answer):
    answer_list = answer.split(',')
    house = answer_list[1].strip()
    house_list = list(house)
    for i in range(len(house_list)):
            if house_list[i] == 'с' or house_list[i] == 'С' or house_list[i] == 'к' or house_list[i] == 'К':
                house_list.pop(i)
                for j in range(i, len(house_list)):
                    house_list.pop(i)
                break
    house = ''.join(house_list)
    answer_list[1] = house
    answer = ' '.join(answer_list)
    return answer

def adress_confirm(answer):
    geocoder = RateLimiter(Nominatim(user_agent='tutorial').geocode, min_delay_seconds=1)
    dictionary = geocoder('Москва, {}'.format(answer)).raw
    house_coord = ' '.join([dictionary['lat'], dictionary['lon']])
    return dictionary, house_coord

def dist_metro(house_coord):
    try:
        keys_list = dist_metro_server(house_coord)[0]
        sorted_dist_metro_dict = dist_metro_server(house_coord)[1]
    except:
        df_metro = pd.read_csv('METRO.csv')
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

@dp.message_handler(text = "Узнать аренду квартиры! 🤪")
async def get_adress_first(message: types.Message):
    await message.answer("Введите улицу и номер дома в формате:\nЗолоторожский Вал, 11с7",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.start_ml.set()

@dp.message_handler(state=MenuButton.start_ml)
async def get_adress_info(message: types.Message, state: FSMContext):
    global dict_df_hard
    if ',' in message.text:
        answer = message.text 
        answer = adress_preobras(answer)
        try:
            dictionary, house_coord = adress_confirm(answer)[0], adress_confirm(answer)[1]
            keys_list, dict_station = dist_metro(house_coord)[0], dist_metro(house_coord)[1]
            if float(dictionary['lat'])<=55.7888532 and float(dictionary['lat'])>=55.7014943:
                dist_kreml = distance.distance(house_coord, coord_kreml).km
                if dist_kreml < 1.5:
                    dict_df_hard['circle_Бульварное'] = 1
                elif dist_kreml < 3 and dist_kreml >= 1.5:
                    dict_df_hard['circle_Садовое'] = 1
                elif dist_kreml >= 3 and dist_kreml < 6:
                    dict_df_hard['circle_3 Транспортное'] = 1
                elif dist_kreml >= 6 and dist_kreml <= 15:
                    dict_df_hard['circle_В пределах МКАД'] = 1
                else:
                    dict_df_hard['circle_За МКАД'] = 1
                metro_time = st.median([dict_station[keys_list[0]], dict_station[keys_list[1]], dict_station[keys_list[2]]])
                dict_df_hard['metro_time'] = metro_time
                dictionary = dictionary['display_name'].split(', ')
                for i in range(len(dictionary)):
                    if "район " or " район" in dictionary[i]:
                        district = dictionary[i]
                        break
                dict_df_hard['disctrict_{}'.format(district.split("район")[0].strip())] = 1
                await state.finish()   
                await message.answer("Выход из состояния")
            else: 
                dist_kreml = distance.distance(house_coord, coord_kreml).km
                if dist_kreml < 1.5:
                    dict_df_hard['circle_Бульварное'] = 1
                elif dist_kreml < 3 and dist_kreml >= 1.5:
                    dict_df_hard['circle_Садовое'] = 1
                elif dist_kreml >= 3 and dist_kreml < 6:
                    dict_df_hard['circle_3 Транспортное'] = 1
                elif dist_kreml >= 6 and dist_kreml <= 17:
                    dict_df_hard['circle_В пределах МКАД'] = 1
                else:
                    dict_df_hard['circle_За МКАД'] = 1
                metro_time = st.median([dict_station[keys_list[0]], dict_station[keys_list[1]], dict_station[keys_list[2]]])
                dict_df_hard['metro_time'] = metro_time
                dictionary = dictionary['display_name'].split(', ')
                for i in range(len(dictionary)):
                    if "район " or " район" in dictionary[i]:
                        district = dictionary[i]
                        break
                dict_df_hard['disctrict_{}'.format(district.split("район")[0].strip()] = 1
                await state.finish()
                await message.answer("Выход из состояния")
        except AttributeError:
            await message.answer('Адрес не найден. Повторите ввод')    
    else:
        await message.answer('Проверьте формат ввода')

            

        
    
    
