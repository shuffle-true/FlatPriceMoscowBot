import logging
import time
from aiogram import types
import operator
import statistics as st
from data.all_config import columns, columns_1, columns_1_0

## модули отвечающие за удаление сообщения
from contextlib import suppress
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from keyboards.default import menu_confirm_start_ml, menu_first, menu_confirm
from keyboards.inline import zalog, comissions, predoplata, lift, count_room, type_of_room, type_of_repair, view_window, \
    type_of_house, type_of_parking, mebel_room, mebel_kitchen, balcony
from keyboards.inline.callback_dates import choice_callback
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import dp
from states import MenuButton
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from geopy import distance
import ssl
import pandas as pd
from .lol import answer_ml
from numpy import random as rnd

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
    df_metro = pd.read_csv('METRO.csv')
    dist_metro = {}
    for i in range(df_metro.shape[0]):
        dist_metro[df_metro['station_name'][i]] = round(distance.distance(df_metro['coord'][i], house_coord).km,
                                                        2)
    sorted_dist_metro_tuple = sorted(dist_metro.items(), key=operator.itemgetter(1))
    sorted_dist_metro_dict = OrderedDict()
    for k, v in sorted_dist_metro_tuple:
        sorted_dist_metro_dict[k] = v
    keys_list = list(sorted_dist_metro_dict.keys())
    return keys_list, sorted_dist_metro_dict


@dp.message_handler(text="Узнать аренду квартиры! 🤪")
async def get_adress_first(message: types.Message):
    await message.answer("Введите улицу и номер дома в формате:\nЗолоторожский Вал, 11с7",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.start_ml.set()


@dp.message_handler(state=MenuButton.start_ml)
async def get_adress_info(message: types.Message, state: FSMContext):
    if ',' in message.text:
        async with state.proxy() as data:
            for i in range(len(columns)):
                data[columns[i]] = 0
        answer = message.text
        answer = adress_preobras(answer)
        try:
            dictionary, house_coord = adress_confirm(answer)[0], adress_confirm(answer)[1]
            keys_list, dict_station = dist_metro(house_coord)[0], dist_metro(house_coord)[1]
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
                metro_time = st.median(
                    [dict_station[keys_list[0]], dict_station[keys_list[1]], dict_station[keys_list[2]]])
                async with state.proxy() as data:
                    data['metro_time'] = metro_time
                dictionary = dictionary['display_name'].split(', ')
                for i in range(len(dictionary)):
                    if "район " or " район" in dictionary[i]:
                        district = dictionary[i]
                        break
                district = district.split("район")[0].strip()
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
                metro_time = st.median(
                    [dict_station[keys_list[0]], dict_station[keys_list[1]], dict_station[keys_list[2]]])
                async with state.proxy() as data:
                    data['metro_time'] = metro_time
                dictionary = dictionary['display_name'].split(', ')
                for i in range(len(dictionary)):
                    if ("район " or " район") in dictionary[i]:
                        district = dictionary[i]
                        break
                district = district.split("район")[0].strip()
                df_1 = pd.read_csv('DISTRICT.csv')
                df_1 = df_1[columns_1]
                df_1_dict = dict(df_1)
                for i in range(len(df_1_dict['Название района'])):
                    if district in df_1_dict['Название района'][i]:
                        oper = i

                for i in range(len(columns_1_0)):
                    async with state.proxy() as data:
                        data[columns_1_0[i]] = df_1_dict[columns_1_0[i]][oper]
                await message.answer("""Для прогнозирования требуется некоторая информация о квартире. \n\nСейчас вам будет 
предложено ввести данные о мебели, этаже, наличие ванных комнат и т.д.""")
                # time.sleep(5)
                await message.answer("Укажите залог", reply_markup=zalog)
        except AttributeError:
            await message.answer('Адрес не найден. Повторите ввод')
    else:
        await message.answer('Проверьте формат ввода')




@dp.callback_query_handler(choice_callback.filter(name="zalog"), state = [MenuButton.start_ml])
async def get_zalog_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    zalog = callback_data["count"]
    async with state.proxy() as data:
        data['Залог'] = zalog
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите информацию о комиссии",
                              reply_markup=comissions)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="comissions"), state = [MenuButton.start_ml])
async def get_comissoins_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    comissions = callback_data["count"]
    async with state.proxy() as data:
        data['Комиссия'] = comissions
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите информацию о предоплате",
                              reply_markup=predoplata)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="prepay"), state = [MenuButton.start_ml])
async def get_prepay_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    prepay = callback_data["count"]
    async with state.proxy() as data:
        data['Предоплата'] = prepay
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите информацию о лифтах",
                              reply_markup=lift)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="lift"), state = [MenuButton.start_ml])
async def get_lift_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    lift = callback_data["count"]
    async with state.proxy() as data:
        data['elevators'] = lift
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nСколько комнат в квартире?",
                              reply_markup=count_room)
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="room"), state = [MenuButton.start_ml])
async def get_room_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    count_room = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nУкажите тип жилого помещения", reply_markup = type_of_room)
    async with state.proxy() as data:
        data['count_room'] = count_room
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

@dp.callback_query_handler(choice_callback.filter(name="type_of_room"), state = [MenuButton.start_ml])
async def get_type_of_room_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_of_room = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nКакой в квартире ремонт?", reply_markup = type_of_repair)
    if type_of_room == 0:
        async with state.proxy() as data:
            data['type_of_housing_Квартира'] = 1
    elif type_of_room == 1:
        async with state.proxy() as data:
            data['type_of_housing_Студия'] = 1
    else:
        async with state.proxy() as data:
            data['type_of_housing_Апартаменты'] = 1
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="type_of_repair"), state = [MenuButton.start_ml])
async def get_type_of_repair_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_of_repair = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nКуда выходят окна?", reply_markup = view_window)
    if type_of_repair == 0:
        async with state.proxy() as data:
            data['repair_flat_Косметический'] = 1
    elif type_of_repair == 1:
        async with state.proxy() as data:
            data['repair_flat_Евроремонт'] = 1
    elif type_of_repair == 2:
        async with state.proxy() as data:
            data['repair_flat_Дизайнерский'] = 1
    else:
        async with state.proxy() as data:
            data['repair_flat_Без ремонта'] = 1
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

@dp.callback_query_handler(choice_callback.filter(name="view_window"), state = [MenuButton.start_ml])
async def get_view_window_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_of_repair = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВыберите тип дома", reply_markup = type_of_house)
    if type_of_room == 0:
        async with state.proxy() as data:
            data['view_outside_Во двор'] = 1
    elif type_of_room == 1:
        async with state.proxy() as data:
            data['view_outside_На улицу'] = 1
    else:
        async with state.proxy() as data:
            data['view_outside_На улицу и двор'] = 1
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="type_of_house"), state = [MenuButton.start_ml])
async def get_type_of_house_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_of_house = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВыберите тип парковки", reply_markup = type_of_parking)
    if type_of_house == 0:
        async with state.proxy() as data:
            data['type_house_Блочный'] = 1
    elif type_of_house == 1:
        async with state.proxy() as data:
            data['type_house_Кирпичный'] = 1
    elif type_of_house == 2:
        async with state.proxy() as data:
            data['type_house_Деревянный'] = 1
    elif type_of_house == 3:
        async with state.proxy() as data:
            data['type_house_Панельный'] = 1
    elif type_of_house == 4:
        async with state.proxy() as data:
            data['type_house_Сталинский'] = 1
    elif type_of_house == 6:
        async with state.proxy() as data:
            data['type_house_Монолитный'] = 1
    elif type_of_house == 7:
        async with state.proxy() as data:
            data['type_house_Монолитно кирпичный'] = 1
    else:
        async with state.proxy() as data:
            data['type_house_Старый фонд'] = 1
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="type_of_parking"), state = [MenuButton.start_ml])
async def get_type_of_parking_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    type_of_parking = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nМебель в комнатах",
                              reply_markup=mebel_room)
    if type_of_parking == 2:
        async with state.proxy() as data:
            data['parking_Открытая'] = 1
    elif type_of_parking == 1:
        async with state.proxy() as data:
            data['parking_Подземная'] = 1
    elif type_of_parking == 3:
        async with state.proxy() as data:
            data['parking_Многоуровневая'] = 1
    else:
        async with state.proxy() as data:
            data['parking_Наземная'] = 1
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(choice_callback.filter(name="mebel_room"), state = [MenuButton.start_ml])
async def get_mebel_room_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    mebel_room = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nМебель на кухне",
                              reply_markup=mebel_kitchen)
    if mebel_room == 0:
        async with state.proxy() as data:
            data['Мебель в комнатах'] = 1
    else:
        async with state.proxy() as data:
            data['Мебель в комнатах'] = 0
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

@dp.callback_query_handler(choice_callback.filter(name="mebel_kitchen"), state = [MenuButton.start_ml])
async def get_mebel_kitchen_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    mebel_kitchen = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nИмеется ли балкон?",
                              reply_markup=balcony)
    if mebel_kitchen == 0:
        async with state.proxy() as data:
            data['Мебель на кухне'] = 1
    else:
        async with state.proxy() as data:
            data['Мебель на кухне'] = 0
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

@dp.callback_query_handler(choice_callback.filter(name="balcony"), state = [MenuButton.start_ml])
async def get_balcony_info(call: CallbackQuery, callback_data: dict, state: FSMContext):
    balcony = callback_data["count"]
    await call.message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\nВведите площадь (можно примерную) квартиры, этаж и год постройки "
                              f"дома через пробел. \n\nПример:\n52 12 2016",
                              reply_markup=ReplyKeyboardRemove())
    if balcony == 0:
        async with state.proxy() as data:
            data['balcony'] = 1
    else:
        async with state.proxy() as data:
            data['balcony'] = 0
    await MenuButton.start_info_for_ml.set()
    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()

@dp.message_handler(state = MenuButton.start_info_for_ml)
async def get_square_info(message: types.Message, state: FSMContext):
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
    df.to_excel('{}.xlsx'.format(message.from_user.id), index=False)
    await state.finish()
    await message.answer("Информация получена! Ожидайте")















# async with state.proxy() as df:
#     df = pd.DataFrame()
# df = df.append(data.as_dict(), ignore_index=True)
# df.to_excel('{}.xlsx'.format(call.from_user.id), index=False)
# await state.finish()
