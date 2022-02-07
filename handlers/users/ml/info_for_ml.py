# модули для корректного обращения к API бота
from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import dp

## модули отвечающие за удаление сообщения
from contextlib import suppress
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

# модули для взаимодействия с пользователем
from keyboards.inline import zalog, comissions, predoplata, lift, count_room, type_of_room, type_of_repair, view_window, \
    type_of_house, type_of_parking, mebel_room, mebel_kitchen, balcony # импорт всех инлайн клавиуатур, используемых в скрипте
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

# модули содержащие доп информацию
from data.all_config import columns, columns_1, columns_1_0
from .lol import answer_ml

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


@dp.message_handler(text="Узнать аренду квартиры! 🤪")
async def start_get_info(message: types.Message):
    await message.answer("Введите улицу и номер дома в формате:\nЗолоторожский Вал, 11с7",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.start_ml.set()


@dp.message_handler(state=MenuButton.start_ml)
async def get_adress_info(message: types.Message, state: FSMContext):
    if ',' in message.text:
        answr = Preobras()

        async with state.proxy() as data:
            for i in range(len(columns)):
                data[columns[i]] = 0

        answer = answr.adress_preobras(message.text)

        try:
            dictionary, house_coord = answr.adress_info(answer)
            keys_list, dict_station = answr.dist_metro(house_coord)

            if float(dictionary['lat']) <= 55.7888532 and float(dictionary['lat']) >= 55.7014943:
                dist_kreml = distance.distance(house_coord, coord_kreml).km

                if dist_kreml < 1.5:
                    async with state.proxy() as data:
                        data['circle_Бульварное'] = 1

                elif dist_kreml < 3 and dist_kreml >= 1.5:
                    async with state.proxy() as data:
                        data['circle_Садовое'] = 1

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
                    data['metro_time'] = metro_time

                dictionary = dictionary['display_name'].split(', ')

                for i in range(len(dictionary)):
                    if "район " or " район" in dictionary[i]:
                        district = dictionary[i]
                        break

                district = district.split("район")[1].strip()
                df_1 = pd.read_csv('DISTRICT.csv')
                df_1 = df_1[columns_1]
                df_1_dict = dict(df_1)

                for i in range(len(df_1_dict['Название района'])):
                    if district in df_1_dict['Название района'][i]:
                        oper = i

                for i in range(len(columns_1)):
                    async with state.proxy() as data:
                        data[columns_1_0[i]] = df_1_dict[columns_1_0[i]][oper]

                async with state.proxy() as data:
                    data['district_{}'.format(district)] = 1

                await message.answer("""Для прогнозирования требуется некоторая информация о квартире. \n\nСейчас вам будет 
 предложено ввести данные о мебели, этаже, наличие ванных комнат и т.д.""")
                await message.answer("Укажите залог", reply_markup=zalog)

            else:
                dist_kreml = distance.distance(house_coord, coord_kreml).km

                if dist_kreml < 1.5:
                    async with state.proxy() as data:
                        data['circle_Бульварное'] = 1

                elif 3 > dist_kreml >= 1.5:
                    async with state.proxy() as data:
                        data['circle_Садовое'] = 1

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
                    data['metro_time'] = metro_time

                dictionary = dictionary['display_name'].split(', ')

                for i in range(len(dictionary)):
                    if ("район " or " район") in dictionary[i]:
                        district = dictionary[i]
                        break

                district = district.split("район")[1].strip()
                df_1 = pd.read_csv('DISTRICT.csv')
                df_1 = df_1[columns_1]
                df_1_dict = dict(df_1)

                for i in range(len(df_1_dict['Название района'])):
                    if district in df_1_dict['Название района'][i]:
                        oper = i

                for i in range(len(columns_1_0)):
                    async with state.proxy() as data:
                        data[columns_1_0[i]] = df_1_dict[columns_1_0[i]][oper]

                async with state.proxy() as data:
                    data['district_{}'.format(district)] = 1

                await message.answer("""Для прогнозирования требуется некоторая информация о квартире. \n\nСейчас вам будет 
предложено ввести данные о мебели, этаже, наличие ванных комнат и т.д.""")
                # time.sleep(5)
                await message.answer("Укажите залог", reply_markup=zalog)

        except AttributeError:
            await message.answer('Адрес не найден. Повторите ввод')

    else:
        await message.answer('Проверьте формат ввода')




@dp.callback_query_handler(choice_callback.filter(name="zalog"), state = [MenuButton.start_ml])
async def get_zalog(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['Залог'] = callback_data["count"]

    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите информацию о комиссии",
                              reply_markup=comissions)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="comissions"), state = [MenuButton.start_ml])
async def get_comissions(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['Комиссия'] = callback_data["count"]

    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите информацию о предоплате",
                              reply_markup=predoplata)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="prepay"), state = [MenuButton.start_ml])
async def get_prepay(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['Предоплата'] = callback_data["count"]

    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите информацию о лифтах",
                              reply_markup=lift)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="lift"), state = [MenuButton.start_ml])
async def get_lift(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        data['elevators'] = callback_data["count"]

    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nСколько комнат в квартире?",
                              reply_markup=count_room)

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="room"), state = [MenuButton.start_ml])
async def get_room(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите тип жилого помещения", reply_markup = type_of_room)

    async with state.proxy() as data:
        data['count_room'] = callback_data["count"]

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

@dp.callback_query_handler(choice_callback.filter(name="type_of_room"), state = [MenuButton.start_ml])
async def get_type_of_room(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nКакой в квартире ремонт?", reply_markup = type_of_repair)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['type_of_housing_Квартира'] = 1

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['type_of_housing_Студия'] = 1

    else:
        async with state.proxy() as data:
            data['type_of_housing_Апартаменты'] = 1

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="type_of_repair"), state = [MenuButton.start_ml])
async def get_type_of_repair(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nКуда выходят окна?", reply_markup = view_window)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['repair_flat_Косметический'] = 1

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['repair_flat_Евроремонт'] = 1

    elif callback_data["count"] == '2':
        async with state.proxy() as data:
            data['repair_flat_Дизайнерский'] = 1

    else:
        async with state.proxy() as data:
            data['repair_flat_Без ремонта'] = 1

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="view_window"), state = [MenuButton.start_ml])
async def get_view_window(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВыберите тип дома", reply_markup = type_of_house)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['view_outside_Во двор'] = 1

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['view_outside_На улицу'] = 1

    else:
        async with state.proxy() as data:
            data['view_outside_На улицу и двор'] = 1

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="type_of_house"), state = [MenuButton.start_ml])
async def get_type_of_house(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВыберите тип парковки", reply_markup = type_of_parking)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['type_house_Блочный'] = 1

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['type_house_Кирпичный'] = 1

    elif callback_data["count"] == '2':
        async with state.proxy() as data:
            data['type_house_Деревянный'] = 1

    elif callback_data["count"] == '3':
        async with state.proxy() as data:
            data['type_house_Панельный'] = 1

    elif callback_data["count"] == '4':
        async with state.proxy() as data:
            data['type_house_Сталинский'] = 1

    elif callback_data["count"] == '6':
        async with state.proxy() as data:
            data['type_house_Монолитный'] = 1

    elif callback_data["count"] == '7':
        async with state.proxy() as data:
            data['type_house_Монолитно кирпичный'] = 1

    else:
        async with state.proxy() as data:
            data['type_house_Старый фонд'] = 1

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="type_of_parking"), state = [MenuButton.start_ml])
async def get_type_of_parking(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите наличие мебели в комнатах",
                              reply_markup=mebel_room)

    if callback_data["count"] == '2':
        async with state.proxy() as data:
            data['parking_Открытая'] = 1

    elif callback_data["count"] == '1':
        async with state.proxy() as data:
            data['parking_Подземная'] = 1

    elif callback_data["count"] == '3':
        async with state.proxy() as data:
            data['parking_Многоуровневая'] = 1

    else:
        async with state.proxy() as data:
            data['parking_Наземная'] = 1

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="mebel_room"), state = [MenuButton.start_ml])
async def get_mebel_room(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nЕсть ли кухонный гарнитур?",
                              reply_markup=mebel_kitchen)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['Мебель в комнатах'] = 1

    else:
        async with state.proxy() as data:
            data['Мебель в комнатах'] = 0

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()





@dp.callback_query_handler(choice_callback.filter(name="mebel_kitchen"), state = [MenuButton.start_ml])
async def get_mebel_kitchen(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите наличие балкона",
                              reply_markup=balcony)

    if callback_data["count"] == '0':
        async with state.proxy() as data:
            data['Мебель на кухне'] = 1

    else:
        async with state.proxy() as data:
            data['Мебель на кухне'] = 0

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
            data['balcony'] = 1

    else:
        async with state.proxy() as data:
            data['balcony'] = 0

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
        data['square'] = square[0]
        data['floor'] = square[1]
        data['built_house'] = square[2]

    async with state.proxy() as df:
        df = pd.DataFrame()

    df = df.append(data.as_dict(), ignore_index=True)
    df.to_excel('{}.xlsx'.format(message.from_user.username), index=False)

    await state.finish()
    await message.answer("Информация получена! Ожидайте")
