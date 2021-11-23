from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import ParserStates
from aiogram.types import ReplyKeyboardRemove
import re
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
    global flat_links
    if int(message.text) > 0 and int(message.text) <= len(flat_links):
        await message.answer('Принято')
    else:
        await message.answer('Проверьте корректность!')