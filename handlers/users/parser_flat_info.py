from loader import dp
from aiogram import types
from aiogram.dispatcher import FSMContext
from states import ParserStates
from aiogram.types import ReplyKeyboardRemove
import re
import numpy as np

def read_flat_links():
    flat_links = open( 'flat_links.txt' ).readlines()
    return flat_links
    

@dp.message_handler(text="Начать парсинг квартир")
async def continue_parser(message: types.Message):
    global count_flat
    # flat_list = read_flat_links()
    # flat_list = np.array(flat_list)
    flat_links = read_flat_links()
    print(len(flat_links[0]))
    print(len(flat_links[1]))
    # count_flat = flat_list.size
    await message.answer(f"""Отлично!\nДля парсинга доступно {count_flat} квартир
Введите столько, сколько необходимо""", reply_markup=ReplyKeyboardRemove())
    await ParserStates.flat_links_ready.set()

@dp.message_handler(state = ParserStates.flat_links_ready)
async def count_flat(message: types.Message, state = FSMContext):
    global count_flat
    if int(message.text) > 0 and int(message.text) <= count_flat:
        await message.answer('Принято')
    else:
        await message.answer('Проверьте корректность!')