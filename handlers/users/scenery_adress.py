import time
from aiogram import types
from aiogram.dispatcher.filters.builtin import Command
from keyboards.default import  menu_adress_second, menu_back_from_random_state, menu_second
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from loader import dp
from states import MenuButton
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
from .config_for_server import dist_metro_server
import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context
from collections import OrderedDict
import operator
coord_kreml = '55.751999 37.617734'
import openpyxl



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

def dist_metro(house_coord):
    try
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

    
def adress_confirm(answer):
    geocoder = RateLimiter(Nominatim(user_agent='tutorial').geocode, min_delay_seconds=1)
    dictionary = geocoder('Москва, {}'.format(answer)).raw
    house_coord = ' '.join([dictionary['lat'], dictionary['lon']])
    dictionary = geocoder('Москва, {}'.format(answer)).raw
    return dictionary, house_coord






@dp.message_handler(text="Ввести адрес 🏠")
async def get_adress_first(message: types.Message):
    await message.answer("Введите улицу и номер дома в формате:\nЗолоторожский Вал, 11с7",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.adress_first.set()



@dp.message_handler(state=[MenuButton.adress_first, MenuButton.adress_second])
async def get_adress_info(message: types.Message, state: FSMContext):
    if ',' in message.text:
        answer = message.text
        answer = adress_preobras(answer)
        try:
            dictionary, house_coord = adress_confirm(answer)[0], adress_confirm(answer)[1]
            await message.answer('Адрес получен. Идет обработка...')
            keys_list, dict_station = dist_metro(house_coord)[0], dist_metro(house_coord)[1]
            if float(dictionary['lat'])<=55.7888532 and float(dictionary['lat'])>=55.7014943:
                dist_kreml = distance.distance(house_coord, coord_kreml).km
                time.sleep(2)
                await message.answer('По вашему запросу найден следующий объект:')
                time.sleep(2)
                if dist_kreml < 1.5:
                    await message.answer('Дом расположен внутри Бульварного кольца')
                elif dist_kreml < 3 and dist_kreml >= 1.5:
                    await message.answer('Дом расположен внутри Садового кольца')
                elif dist_kreml >= 3 and dist_kreml < 6:
                    await message.answer('Дом расположен внутри 3 Транспортного кольца')
                elif dist_kreml >= 6 and dist_kreml <= 15:
                    await message.answer('Дом расположен за пределами 3 Транспортного кольца, но в пределах МКАД')
                else:
                    await message.answer('Дом расположен за МКАД-ом')
            else:
                dist_kreml = distance.distance(house_coord, coord_kreml).km
                time.sleep(2)
                await message.answer('По вашему запросу найден следующий объект:')
                time.sleep(2)
                if dist_kreml < 1.5:
                    await message.answer('Дом расположен внутри Бульварного кольца')
                elif dist_kreml < 3 and dist_kreml >= 1.5:
                    await message.answer('Дом расположен внутри Садового кольца')
                elif dist_kreml >= 3 and dist_kreml < 6:
                    await message.answer('Дом расположен внутри 3 Транспортного кольца')
                elif dist_kreml >= 6 and dist_kreml <= 17:
                    await message.answer('Дом расположен за пределами 3 Транспортного кольца, но в пределах МКАД')
                else:
                    await message.answer('Дом расположен за МКАД-ом')
            time.sleep(2)
            await message.answer('{}'.format(dictionary['display_name']))
            time.sleep(2)
            await message.answer(f"""Его координаты: \n{float(dictionary['lat']):.6f} {float(dictionary['lon']):.6f} \n\nРасстояние до ближайшего метро:\n
{keys_list[0]}: {dict_station[keys_list[0]]} км 
{keys_list[1]}: {dict_station[keys_list[1]]} км 
{keys_list[2]}: {dict_station[keys_list[2]]} км

Пешком до самого ближайшего метро:
{round(dict_station[keys_list[0]]/0.066666666, 2)} мин.

На транспорте до самого ближайшего метро
{round(dict_station[keys_list[0]]/0.333333333, 2)} мин.""", reply_markup=menu_adress_second)
            await state.finish()            
        except AttributeError:
            if message.text == 'Отменить ввод':
                await state.finish()
                await message.answer('Вы вернулись в меню',reply_markup=menu_second)
            else:
                await message.answer('Адрес не найден. Повторите ввод', reply_markup = menu_back_from_random_state)    
    else:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.answer('Вы вернулись в меню',reply_markup=menu_second)
        else:
            await message.answer('Проверьте формат ввода', reply_markup = menu_back_from_random_state)
        


@dp.message_handler(text="Ввести еще один адрес 🏠")
async def get_adress_info_second(message: types.Message):
    await message.answer("Введите улицу и номер дома в формате:\nЗолоторожский Вал, 11с7",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.adress_second.set()