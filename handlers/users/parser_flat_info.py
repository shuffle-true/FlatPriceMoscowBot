from handlers.users.config_for_server import get_flat_server
from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from states import ParserStates
from aiogram.types import ReplyKeyboardRemove, message
from .dataframe_preprocessing import run_preprocessing_script
from .parser import get_flat
from .df_append import df_append
import numpy as np
import pandas as pd

    

@dp.message_handler(text="Начать парсинг квартир")
async def continue_parser(message: types.Message):
    global flat_links
    df_flat_links = pd.read_csv('flat_links_one_questions.csv')
    flat_links = np.array(df_flat_links['links'])
    await message.answer(f"""Отлично!\nДля парсинга доступно {len(flat_links)} квартир
Введите столько, сколько необходимо""", reply_markup=ReplyKeyboardRemove())
    await ParserStates.flat_links_ready.set()

@dp.message_handler(state = ParserStates.flat_links_ready)
async def count_flat(message: types.Message, state = FSMContext):
    global flat_links, df
    if int(message.text) > 0 and int(message.text) <= len(flat_links):
        await message.answer('Принято')
        count_flat = message.text
        for i in range(int(count_flat)):
            try:
                try:
                    soup = get_flat(flat_links, i)
                    df = df_append(soup)
                except AttributeError:
                    pass
            except:
                try:
                    soup = get_flat_server(flat_links, i)
                    df = df_append(soup)
                    await message.answer('Файлы добавлены!')
                except AttributeError:
                    pass
            if i == round(int(count_flat)*0.1):
                await message.answer('Выполнено 10%')
            if i == round(int(count_flat)*0.2):
                await message.answer('Выполнено 20%')
            if i == round(int(count_flat)*0.3):
                await message.answer('Выполнено 30%')
            if i == round(int(count_flat)*0.4):
                await message.answer('Выполнено 40%')
            if i == round(int(count_flat)*0.5):
                await message.answer('Выполнено 50%')
            if i == round(int(count_flat)*0.6):
                await message.answer('Выполнено 60%')
            if i == round(int(count_flat)*0.7):
                await message.answer('Выполнено 70%')
            if i == round(int(count_flat)*0.8):
                await message.answer('Выполнено 80%')
            if i == round(int(count_flat)*0.9):
                await message.answer('Выполнено 90%')
            if i == round(int(count_flat)*0.95):
                await message.answer('Выполнено 95%')
        df.to_csv('DataFrameFlat.csv', index = False)
        df.to_excel('DataFrameFlat.xlsx', index = False)
        await message.answer('Файлы добавлены!')
        await state.finish()
    else:
        await message.answer('Проверьте корректность!')

@dp.message_handler(Command('data_preprocessing'))
async def count_flat(message: types.Message):
    run_preprocessing_script()
    await message.answer ('Предобработка завершена!\nФайлы успешно созданы')

@dp.message_handler(Command("open_df"))
async def get_df_flat(message: types.Document):
    await message.reply_document(open("DataFrameFlat.xlsx","rb"))

@dp.message_handler(Command("open_preprocessing"))
async def save_df_flat(message: types.Document):
    await message.reply_document(open("DataFrame_after_preprocessing.xlsx","rb"))
    await message.reply_document(open("Value_after_preprocessing.xlsx","rb"))