from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from .parser import chrome_open, pages_count, links_flat
from aiogram.dispatcher import FSMContext
from states import ParserStates
from keyboards.default import price_button, confirm_button, menu_second, confirm_algorithm_button, confirm_pars_button
from aiogram.types import ReplyKeyboardRemove 
import re, math
import numpy as np
import pandas as pd
flag_maxprice=0
flag_minprice=0
print('__file__={0:<35} | __name__={1:<25} | __package__={2:<25}'.format(__file__,__name__,str(__package__)))

def get_count_page(soup):
    title = soup.find('title').text
    digit = re.findall(r'\d+', title)
    return digit




@dp.message_handler(Command("pars"))
async def get_chrome(message: types.Message):
    chrome = chrome_open()
    chrome.minimize_window()
    await message.answer('Драйвер запущен в тестовом. \nВыберите действие.', reply_markup = price_button)


@dp.message_handler(text="Ввести нижний порог цены")
async def get_min_price(message: types.Message):
    await message.answer('Укажите нижний порог', reply_markup = ReplyKeyboardRemove())
    await ParserStates.minprice.set()

@dp.message_handler(state = ParserStates.minprice)
async  def enter_min_price(message: types.Message,state=FSMContext):
    global flag_minprice, min_price
    min_price = message.text
    flag_minprice += 1
    if (flag_maxprice == 1 and flag_minprice == 1) or (flag_maxprice == 2 and flag_minprice == 2) or(flag_maxprice == 3 and flag_minprice == 3) or(flag_maxprice == 4 and flag_minprice == 4) or(flag_maxprice == 5 and flag_minprice == 5) or (flag_maxprice == 6 and flag_minprice == 6) or (flag_maxprice == 7 and flag_minprice == 7) or (flag_maxprice == 8 and flag_minprice == 8) or (flag_maxprice == 9 and flag_minprice == 9) or (flag_maxprice == 10 and flag_minprice == 10) or (flag_maxprice == 11 and flag_minprice == 11) or (flag_maxprice == 12 and flag_minprice == 12):
        await message.answer('Данные получены! \nПодтвердите выполнение алгоритма', reply_markup=confirm_button)
    else:
        await message.answer('Выберите дальнейшее действие', reply_markup=price_button)
    await state.finish()


@dp.message_handler(text="Ввести верхний порог цены")
async def get_max_price(message: types.Message):
    await message.answer('Укажите верхний порог', reply_markup = ReplyKeyboardRemove())
    await ParserStates.maxprice.set()


@dp.message_handler(state = ParserStates.maxprice)
async  def enter_max_price(message: types.Message,state=FSMContext):
    global flag_maxprice, max_price
    max_price = message.text
    flag_maxprice += 1
    if (flag_maxprice == 1 and flag_minprice == 1) or (flag_maxprice == 2 and flag_minprice == 2) or(flag_maxprice == 3 and flag_minprice == 3) or(flag_maxprice == 4 and flag_minprice == 4) or(flag_maxprice == 5 and flag_minprice == 5) or (flag_maxprice == 6 and flag_minprice == 6) or (flag_maxprice == 7 and flag_minprice == 7) or (flag_maxprice == 8 and flag_minprice == 8) or (flag_maxprice == 9 and flag_minprice == 9) or (flag_maxprice == 10 and flag_minprice == 10) or (flag_maxprice == 11 and flag_minprice == 11) or (flag_maxprice == 12 and flag_minprice == 12):
        await message.answer('Данные получены! \nПодтвердите выполнение алгоритма', reply_markup=confirm_button)
    else:
        await message.answer('Выберите дальнейшее действие', reply_markup=price_button)
    await state.finish()


  
    

@dp.message_handler(text="Отменить")
async def cancel_start(message: types.Message):
    await message.answer('Хорошо! \nВы будете возвращены в меню', reply_markup=menu_second)



@dp.message_handler(text="Подтвердить")
async def confirm_start(message: types.Message):
    global min_price, max_price, count_pages
    await message.answer('Принято! Начинается обработка...', reply_markup = ReplyKeyboardRemove())
    soup = pages_count(min_price, max_price)
    await message.answer('Код получен!')
    digit_list = get_count_page(soup)
    try:
        digit = ''.join([digit_list[0], digit_list[1]])
    except IndexError:
        digit = digit_list[0]
    count_pages = math.ceil(int(digit) / 28)
    await message.answer(f'В указанном диапазоне найдено {count_pages} страниц.\nПродолжить обработку или изменить порог цены?', 
                                                                                        reply_markup = confirm_algorithm_button)


@dp.message_handler(text="Прервать")
async def cancel_alghoritm(message: types.Message):
    await message.answer('Хорошо! \nВы будете возвращены в меню', reply_markup=menu_second)



@dp.message_handler(text="Продолжить обработку")
async def continue_alghoritm(message: types.Message):
    await message.answer('Ok!\nВведите кол-во страниц для парсинга\nМакс. 55', reply_markup = ReplyKeyboardRemove())
    await ParserStates.continue_alghoritm.set()

@dp.message_handler(state = ParserStates.continue_alghoritm)
async def continue_alghoritm(message: types.Message, state = FSMContext):
    global max_price, min_price
    if message.text.isdigit() and int(message.text) <= 55 and int(message.text) > 1:
        answer_count_page = message.text
        await message.answer(f'Примерное время ожидания {0.16 * int(answer_count_page):.2f} мин')
        df_links_flat = links_flat(max_price, min_price, answer_count_page)
        df_links_flat.to_csv('flat_links_one_questions.csv', index = False)
        await message.answer('Файл со ссылками на квартиры создан успешно!\nПродолжаем?', reply_markup = confirm_pars_button)
        await state.finish()
    else:
        await message.answer('Убедитесь, что введено число и оно не превышает 55')
    

@dp.message_handler(text="Остановить машину!")
async def cancel_parser(message: types.Message):
    await message.answer('Хорошо! \nВы будете возвращены в меню', reply_markup=menu_second)
    



    
