import matplotlib.pyplot as plt
import pandas as pd

from aiogram import types
from aiogram.types import ReplyKeyboardRemove, CallbackQuery
from aiogram.dispatcher import FSMContext
from loader import dp

from keyboards.inline.menu_for_interactive import type_of_graph, OX, OY
from keyboards.inline.callback_dates import matlab_img

from states import MenuButton # импорт машин состояния

## модули отвечающие за удаление сообщения
from contextlib import suppress
from aiogram.utils.exceptions import (MessageCantBeDeleted,
                                      MessageToDeleteNotFound)

from keyboards.default import menu_first


@dp.message_handler(text = "Интерактивчик 😐")
async def get_answer_img(message: types.Message):
    await message.answer("Выберите тип графика:", reply_markup=type_of_graph)
    await MenuButton.start_interactive.set()



@dp.callback_query_handler(matlab_img.filter(name="type_of_graph"), state = [MenuButton.start_interactive])
async def get_type_of_graph(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.answer("Выберите величину по оси Ox:", reply_markup=OX)

    async with state.proxy() as data:
        data['type'] = 0
        data['ox'] = 0
        data['oy'] = 0

    if callback_data['count'] == '0':
        async with state.proxy() as data:
            data['type'] = 'scatter'
    elif callback_data['count'] == '1':
        async with state.proxy() as data:
            data['type'] = 'bar'

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()


@dp.callback_query_handler(matlab_img.filter(name="OX"), state = [MenuButton.start_interactive])
async def get_x(call: CallbackQuery, callback_data: dict, state: FSMContext):
    flag = True
    async with state.proxy() as data:
        if callback_data['count'] == '0':
            async with state.proxy() as data:
                data['ox'] = 'square_log'

        elif callback_data['count'] == '1':
            async with state.proxy() as data:
                data['ox'] = 'floor_log'

        elif callback_data['count'] == '2':
            async with state.proxy() as data:
                data['ox'] = 'price'

        if data['type'] == 'scatter':
            await call.message.answer("Выберите величину по оси Oy:", reply_markup=OY)
            flag = False
        if not flag:
            with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
                await call.message.delete()

    if flag:
        df = pd.read_csv('Ready_for_fit.csv')

        if callback_data['count'] == '0':
            plt.hist('square_log', data = df, bins = 25)
            plt.xlabel('Площадь')
            plt.ylabel('Кол-во')
            plt.title('Распределение площади')
            plt.savefig('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id))
            plt.clf()

            photo = open('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id), 'rb')

            await call.message.reply_photo(photo, reply_markup=menu_first)

        elif callback_data['count'] == '1':
            plt.hist('floor_log', data = df, bins = 25)
            plt.xlabel('Логарифм этажа')
            plt.ylabel('Кол-во')
            plt.title('Распределение этажей')
            plt.savefig('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id))
            plt.clf()

            photo = open('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id), 'rb')

            await call.message.reply_photo(photo, reply_markup=menu_first)

        elif callback_data['count'] == '2':
            plt.hist('price', data = df, bins = 25)
            plt.xlabel('Аренда')
            plt.ylabel('Кол-во')
            plt.title('Распределение арендной платы')
            plt.savefig('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id))
            plt.clf()

            photo = open('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id), 'rb')

            await call.message.reply_photo(photo, reply_markup=menu_first)

        await state.finish()

        with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
            await call.message.delete()

@dp.callback_query_handler(matlab_img.filter(name="OY"), state = [MenuButton.start_interactive])
async def get_y(call: CallbackQuery, callback_data: dict, state: FSMContext):
    async with state.proxy() as data:
        ox = data['ox']

    if callback_data['count'] == '0':
        oy = 'metro_time_log'
    df = pd.read_csv('Ready_for_fit.csv')

    plt.scatter(ox, oy,
                data=df)
    plt.xlabel(ox)
    plt.ylabel(oy)
    plt.title('Заданное распределение')

    plt.savefig('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id))
    plt.clf()

    photo = open('IMG_INTERACTIVE/{}.png'.format(call.message.from_user.id), 'rb')

    await call.message.reply_photo(photo, reply_markup=menu_first)

    await state.finish()

    with suppress(MessageCantBeDeleted, MessageToDeleteNotFound):
        await call.message.delete()
