﻿# модули для корректного обращения к API бота
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import dp

## модули отвечающие за удаление сообщения
from contextlib import suppress
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from keyboards.default import menu_first

# модули для взаимодействия с пользователем
from keyboards.inline import zalog, comissions, count_room, type_of_repair, view_window, \
    type_of_house, type_of_parking, mebel_room, balcony # импорт всех инлайн клавиуатур, используемых в скрипте
from keyboards.inline.callback_dates import choice_callback # импорт callback_data для определения того, что ввел пользователь
from states import MenuButton # импорт машин состояния


# модули для геокодирования, подсчета расстояния и сортировки расстояния для метро
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
from collections import OrderedDict
import operator

# стандартные библиотеки для обработки таблиц и рандом
import pandas as pd
from numpy import random as rnd
import numpy as np

# нахождение азимута
import math

# модули содержащие доп информацию
from data.all_config import columns, columns_1, columns_1_0, columns_2_0, columns_2
from .lol import answer_ml
from .ml_predict import predict

from typing import Dict, List

## Кремлевские координаты
coord_kreml = '55.751999 37.617734'

class Preobras:
    """
    Класс преобразования данных, введенных пользователем
    для дальнейшей передачи в модель
    """
    def __init__(self) -> None:
        pass

    def adress_preobras(self, answer: str) -> str:
        """
        Метод преобразования адреса.

        У номера дома убирает различные буквы, по типу "С", "с", "к", "К".

        Parametrs
        -------------------
        answer: str - адрес дома, введенный пользователем

        Returns
        -------------------
        answer: str - преобразованный адрес дома

        Examples
        -------------------
        >>> Золоторожский вал, 17с8к2
        >>> Золоторожский вал, 17
        """
        self.answer_list = answer.split(',')
        self.house = self.answer_list[1].strip()
        self.house_list = list(self.house)


        for i in range(len(self.house_list)):

            if self.house_list[i] == 'с' or self.house_list[i] == 'С' or self.house_list[i] == 'к' or self.house_list[i] == 'К':
                self.house_list.pop(i)

                for j in range(i, len(self.house_list)):
                    self.house_list.pop(i)
                break

        house = ''.join(self.house_list)
        self.answer_list[1] = house
        self.answer = ' '.join(self.answer_list)

        return self.answer


    def adress_info(self, answer: str) -> [Dict, str]:
        """
        Метод получает информацию о квартире по ее адресу, используя GeoPy

        Parametrs
        ----------------
        answer: str - адрес дома, введенный пользователем

        Returns
        ----------------
        dictionary: Dict - словарь, содержащий геоинформацию о доме
        house_coord: str - строка с координатами дома

        Examples
        ----------------
        >>> Золоторожский вал, 17
        >>> dictionary
        >>> 55.167984 38.167946
        """

        self.geocoder = RateLimiter(Nominatim(user_agent='tutorial').geocode, min_delay_seconds = 2)
        self.dictionary = self.geocoder('Москва, {}'.format(answer)).raw
        self.house_coord = ' '.join([self.dictionary['lat'], self.dictionary['lon']])

        return self.dictionary, self.house_coord


    def dist_metro(self, house_coord: str) -> [List[str], Dict]:
        """
        Метод подсчета расстояния до метро

        Parametrs
        ----------------
        house_coord: str - строка с координатами дома

        Returns
        ----------------
        keys_list: List[str] - отсортированный список названий ближайших станций
        sorted_dist_metro_dict: Dict - отсортированный словарь ближайших станций

        """
        self.df_metro = pd.read_csv('METRO.csv')
        self.dist_metro = {}

        for i in range(self.df_metro.shape[0]):
            self.dist_metro[self.df_metro['station_name'][i]] = round(
                distance.distance(self.df_metro['coord'][i], house_coord).km,2)

        self.sorted_dist_metro_tuple = sorted(self.dist_metro.items(), key=operator.itemgetter(1))
        self.sorted_dist_metro_dict = OrderedDict()

        for key, value in self.sorted_dist_metro_tuple:
            self.sorted_dist_metro_dict[key] = value

        self.keys_list = list(self.sorted_dist_metro_dict.keys())

        return self.keys_list, self.sorted_dist_metro_dict

    def get_azimuth(self, latitude, longitude):

        rad = 6372795

        llat1 = 55.7522
        llong1 = 37.6156
        llat2 = float(latitude)
        llong2 = float(longitude)

        lat1 = llat1 * math.pi / 180.
        lat2 = llat2 * math.pi / 180.
        long1 = llong1 * math.pi / 180.
        long2 = llong2 * math.pi / 180.

        cl1 = math.cos(lat1)
        cl2 = math.cos(lat2)
        sl1 = math.sin(lat1)
        sl2 = math.sin(lat2)
        delta = long2 - long1
        cdelta = math.cos(delta)
        sdelta = math.sin(delta)

        y = math.sqrt(math.pow(cl2 * sdelta, 2) + math.pow(cl1 * sl2 - sl1 * cl2 * cdelta, 2))
        x = sl1 * sl2 + cl1 * cl2 * cdelta
        ad = math.atan2(y, x)

        x = (cl1 * sl2) - (sl1 * cl2 * cdelta)
        y = sdelta * cl2
        z = math.degrees(math.atan(-y / x))

        if (x < 0):
            z = z + 180.

        z2 = (z + 180.) % 360. - 180.
        z2 = - math.radians(z2)
        anglerad2 = z2 - ((2 * math.pi) * math.floor((z2 / (2 * math.pi))))
        angledeg = (anglerad2 * 180.) / math.pi

        return round(angledeg, 2)


@dp.message_handler(text="Самостоятельный ввод")
async def start_get_info(message: types.Message):
    await message.answer("Введите улицу и номер дома в формате:\nЗолоторожский Вал, 11с7",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.start_ml.set()


@dp.message_handler(state=MenuButton.start_ml)
async def get_adress_info(message: types.Message, state: FSMContext):
    if ',' in message.text:
        answr = Preobras()

        async with state.proxy() as data:
            for i in range(len(columns) - 1):
                data[columns[i]] = 0

        answer = answr.adress_preobras(message.text)

        try:
            dictionary, house_coord = answr.adress_info(answer)
            keys_list, dict_station = answr.dist_metro(house_coord)
            if float(dictionary['lat']) <= 55.7888532 and float(dictionary['lat']) >= 55.7014943:
                dist_kreml = distance.distance(house_coord, coord_kreml).km
                if dist_kreml > 20:
                    await message.answer("По указанному адресу найдена квартира за пределами МКАД.\n\nВозможные причины:\n"
                                         "1. Данный адрес находится не в Москве.\n2. В моей базе нет такого адреса. Поправим позже.")
                    await MenuButton.start_ml.finish()


                azimut = answr.get_azimuth(dictionary['lat'], dictionary['lon'])
                async with state.proxy() as data:
                    data['azdist_log'] = np.log(dist_kreml * azimut)
                if dist_kreml < 1.5:
                    async with state.proxy() as data:
                        data['circle_Бульварное'] = 1

                    await message.answer(
                        "*Я работаю в ценовом диапазоне до 120 тыс.руб.\nУказанный адрес находится в центре Москвы "
                        "и есть вероятность, что прогноз может сильно отличаться от истинной цены!*", parse_mode='Markdown')

                elif dist_kreml < 3 and dist_kreml >= 1.5:
                    async with state.proxy() as data:
                        data['circle_Садовое'] = 1

                    await message.answer(
                        "*Я работаю в ценовом диапазоне до 120 тыс.руб.\nУказанный адрес находится в центре Москвы "
                        "и есть вероятность, что прогноз может сильно отличаться от истинной цены!*", parse_mode='Markdown')

                elif dist_kreml >= 3 and dist_kreml < 6:
                    async with state.proxy() as data:
                        data['circle_3 Транспортное'] = 1

                elif dist_kreml >= 6 and dist_kreml <= 15:
                    async with state.proxy() as data:
                        data['circle_В пределах МКАД'] = 1

                else:
                    async with state.proxy() as data:
                        data['circle_За МКАД'] = 1

                metro_time = round(dict_station[keys_list[0]] / 0.066666666, 2)

                async with state.proxy() as data:
                    data['metro_time_log'] = np.log(metro_time)

                dictionary = dictionary['display_name'].split(', ')
                print(dictionary)
                for i in range(len(dictionary)):
                    if ("район " in dictionary[i]) or (" район" in dictionary[i]):
                        district = dictionary[i]
                        break
                    if ('Тропарёво-Никулино' in dictionary[i]):
                        district = 'район Тропарёво-Никулино'
                        break
                try:
                    district = district.split("район")[1].strip()
                    district = district.replace('ё', 'е')
                    df_1 = pd.read_csv('DISTRICT.csv')
                    df_1 = df_1[columns_1]
                    df_1_dict = dict(df_1)



                    for i in range(len(df_1_dict['Название района'])):
                        if district in df_1_dict['Название района'][i]:
                            oper = i

                    for i in range(len(columns_1_0)):
                        async with state.proxy() as data:
                            data[columns_1_0[i]] = df_1_dict[columns_1_0[i]][oper]

                    df_2 = pd.read_excel('DISTRICT_COEF_.xlsx')
                    df_2_dict = dict(df_2)

                    for i in range(len(df_2_dict['district'])):
                        if district in df_2_dict['district'][i]:
                            oper = i

                    for i in range(len(columns_2_0)):
                        async with state.proxy() as data:
                            data[columns_2_0[i]] = df_2_dict[columns_2_0[i]][oper]

                    async with state.proxy() as data:
                        data['mpa'] = df_2_dict['mpa'][oper]

                        await message.answer("""Для прогнозирования требуется некоторая информация о квартире. \n\nСейчас вам будет 
предложено ввести данные о мебели, этаже, наличие ванных комнат и т.д.""")
                        await message.answer("Укажите коммисию", reply_markup=comissions)

                except UnboundLocalError:
                    await message.answer("*Район не определен*", parse_mode="Markdown", reply_markup=menu_first)
                    await state.finish()

            else:
                dist_kreml = distance.distance(house_coord, coord_kreml).km
                azimut = answr.get_azimuth(dictionary['lat'], dictionary['lon'])

                if dist_kreml > 20:
                    await message.answer("По указанному адресу найдена квартира за пределами МКАД.\n\nВозможные причины:\n"
                                         "1. Данный адрес находится не в Москве.\n2. В моей базе нет такого адреса. Поправим позже.")
                    await MenuButton.start_ml.finish()

                async with state.proxy() as data:
                    data['azdist_log'] = np.log(dist_kreml * azimut)

                if dist_kreml < 1.5:
                    async with state.proxy() as data:
                        data['circle_Бульварное'] = 1

                    await message.answer(
                        "*Я работаю в ценовом диапазоне до 120 тыс.руб.\nУказанный адрес находится в центре Москвы "
                        "и есть вероятность, что прогноз может сильно отличаться от истинной цены!*", parse_mode='Markdown')

                elif 3 > dist_kreml >= 1.5:
                    async with state.proxy() as data:
                        data['circle_Садовое'] = 1

                    await message.answer("*Я работаю в ценовом диапазоне до 120 тыс.руб.\nУказанный адрес находится в центре Москвы "
                                         "и есть вероятность, что прогноз может сильно отличаться от истинной цены!*", parse_mode='Markdown')

                elif 3 <= dist_kreml < 6:
                    async with state.proxy() as data:
                        data['circle_3 Транспортное'] = 1

                elif 6 <= dist_kreml <= 17:
                    async with state.proxy() as data:
                        data['circle_В пределах МКАД'] = 1

                else:
                    async with state.proxy() as data:
                        data['circle_За МКАД'] = 1

                metro_time = round(dict_station[keys_list[0]] / 0.066666666, 2)

                async with state.proxy() as data:
                    data['metro_time_log'] = np.log(metro_time)


                dictionary = dictionary['display_name'].split(', ')
                print(dictionary)

                for i in range(len(dictionary)):
                    if ("район " in dictionary[i]) or (" район" in dictionary[i]):
                        district = dictionary[i]
                        break

                    if ('Тропарёво-Никулино' in dictionary[i]):
                        district = 'район Тропарёво-Никулино'
                        break

                try:
                    district = district.split("район")[1].strip()
                    district = district.replace('ё', 'е')
                    df_1 = pd.read_csv('DISTRICT.csv')
                    df_1 = df_1[columns_1]
                    df_1_dict = dict(df_1)


                    for i in range(len(df_1_dict['Название района'])):
                        if district in df_1_dict['Название района'][i]:
                            oper = i

                    for i in range(len(columns_1_0)):
                        async with state.proxy() as data:
                            data[columns_1_0[i]] = df_1_dict[columns_1_0[i]][oper]

                    df_2 = pd.read_excel('DISTRICT_COEF_.xlsx')
                    df_2_dict = dict(df_2)

                    for i in range(len(df_2_dict['district'])):
                        if district in df_2_dict['district'][i]:
                            oper = i

                    for i in range(len(columns_2_0)):
                        async with state.proxy() as data:
                            data[columns_2_0[i]] = df_2_dict[columns_2_0[i]][oper]

                    async with state.proxy() as data:
                        data['mpa'] = df_2_dict['mpa'][oper]

                    await message.answer("""Для прогнозирования требуется некоторая информация о квартире. \n\nСейчас вам будет 
предложено ввести данные о мебели, этаже, наличие ванных комнат и т.д.""")

                    await message.answer("Укажите коммисию", reply_markup=comissions)

                except UnboundLocalError:
                    await message.answer("*Район не определен*", parse_mode="Markdown", reply_markup=menu_first)
                    await state.finish()

        except AttributeError:
            await message.answer('Адрес не найден. Повторите ввод')

    else:
        await message.answer('Проверьте формат ввода')



@dp.callback_query_handler(choice_callback.filter(name="comissions"), state = [MenuButton.start_ml])
async def get_comissions(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['Комиссия'] = float(callback_data["count"])

    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите кол-во комнат.",
                              reply_markup=count_room)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()



@dp.callback_query_handler(choice_callback.filter(name="room"), state = [MenuButton.start_ml])
async def get_room(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nКакой в квартире ремонт?", reply_markup = type_of_repair)

    async with state.proxy() as data:
        data['count_room'] = float(callback_data["count"])

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()



@dp.callback_query_handler(choice_callback.filter(name="type_of_repair"), state = [MenuButton.start_ml])
async def get_type_of_repair(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nКуда выходят окна?", reply_markup = view_window)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['repair_flat_Косметический'] = float(1)

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['repair_flat_Евроремонт'] = float(1)

    elif callback_data["count"] == '2':
        async with state.proxy() as data:
            data['repair_flat_Дизайнерский'] = float(1)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="view_window"), state = [MenuButton.start_ml])
async def get_view_window(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВыберите тип дома", reply_markup = type_of_house)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['view_outside_Во двор'] = float(1)

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['view_outside_На улицу'] = float(1)

    else:
        async with state.proxy() as data:
            data['view_outside_На улицу и двор'] = float(1)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="type_of_house"), state = [MenuButton.start_ml])
async def get_type_of_house(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВыберите тип парковки", reply_markup = type_of_parking)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['type_house_Блочный'] = float(1)

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['type_house_Кирпичный'] = float(1)


    elif callback_data["count"] == '3':
        async with state.proxy() as data:
            data['type_house_Панельный'] = float(1)

    elif callback_data["count"] == '4':
        async with state.proxy() as data:
            data['type_house_Сталинский'] = float(1)

    elif callback_data["count"] == '6':
        async with state.proxy() as data:
            data['type_house_Монолитный'] = float(1)

    elif callback_data["count"] == '7':
        async with state.proxy() as data:
            data['type_house_Монолитно кирпичный'] = float(1)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="type_of_parking"), state = [MenuButton.start_ml])
async def get_type_of_parking(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите наличие мебели в комнатах",
                              reply_markup=mebel_room)

    if callback_data["count"] == '2':
        async with state.proxy() as data:
            data['parking_Открытая'] = float(1)

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['parking_Подземная'] = float(1)


    else:
        async with state.proxy() as data:
            data['parking_Наземная'] = float(1)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="mebel_room"), state = [MenuButton.start_ml])
async def get_mebel_room(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}"
                              f"\n\nУкажите наличие балкона", reply_markup=balcony)
    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['Наличие мебели'] = float(1)

    else:
        async with state.proxy() as data:
            data['Наличие мебели'] = float(0)


    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()



@dp.callback_query_handler(choice_callback.filter(name="balcony"), state = [MenuButton.start_ml])
async def get_balcony(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}"
                              f"\n\nВведите площадь (можно примерную) квартиры, этаж и год постройки "
                              f"дома через пробел. \n\nПример:\n52 12 2016",
                              reply_markup=ReplyKeyboardRemove())

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['balcony'] = float(1)

    else:
        async with state.proxy() as data:
            data['balcony'] = float(0)

    await MenuButton.start_info_for_ml.set()

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.message_handler(state = MenuButton.start_info_for_ml)
async def get_square_floor_year__build(message: types.Message, state: FSMContext):
    square = message.text
    square = square.split(' ')

    for i in range(len(square)):
        if square[i].isdigit() is False:
            await message.answer("Проверьте формат ввода")

    async with state.proxy() as data:
        data['square_log'] = float(square[0])
        data['floor_log'] = np.log(float(square[1]) + 1e-7)
        data['built_house'] = float(square[2])
        data['mpa'] = (data['mpa'] / 40) * float(square[0])



    async with state.proxy() as df:
        df = pd.DataFrame()

    df = df.append(data.as_dict(), ignore_index=True)
    df = df[columns]
    df.to_excel('USER_REQUEST/{}.xlsx'.format(message.from_user.username), index=False)

    await state.finish()
    await message.answer("Информация получена! Ожидайте")

    ans = predict(message.from_user.username)
    await message.answer(f"*Decision Tree O(1): {ans[0]} руб.\n"
                         f"Decision Tree O(N  log N): {ans[1]} руб.\n"
                         f"AdaDecision Tree O(1): No solution.\n"
                         f"Bagging Tree O(10N log N): {ans[2]}\n"
                         f"Bagging Tree O(50N log N): {ans[3]}\n"
                         f"Bagging Tree O(100N log N): {ans[4]}\n"
                         f"Mean for all model: {round(np.mean(ans), 0)}\n"
                         f"Standart Deviation: {round(np.var(ans) ** 0.5, 0)}*", parse_mode='Markdown', reply_markup=menu_first)
