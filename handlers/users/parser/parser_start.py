from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from .parser import Parser
from aiogram.dispatcher import FSMContext
from states import ParserStates
from keyboards.default import price_button, confirm_button, menu_first, confirm_algorithm_button, confirm_pars_button
from aiogram.types import ReplyKeyboardRemove 
import re, math
from data.config import admins
flag_maxprice=0
flag_minprice=0

def get_count_page(soup):
    """
    Получаем кол-во страниц в заданном ценовом диапазоне
    """

    title = soup.find('title').text
    digit = re.findall(r'\d+', title)

    return digit




@dp.message_handler(Command("pars"), user_id=admins)
async def get_chrome(message: types.Message):
    global pars

    pars = Parser()
    pars.chrome_open()

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

    if (flag_maxprice == 1 and flag_minprice == 1) or (flag_maxprice == 2 and flag_minprice == 2) or(flag_maxprice == 3 and flag_minprice == 3) or(flag_maxprice == 4 and flag_minprice == 4) or(flag_maxprice == 5 and flag_minprice == 5) or (flag_maxprice == 6 and flag_minprice == 6) or (flag_maxprice == 7 and flag_minprice == 7) or (flag_maxprice == 8 and flag_minprice == 8) or (flag_maxprice == 9 and flag_minprice == 9) or (flag_maxprice == 10 and flag_minprice == 10) or (flag_maxprice == 11 and flag_minprice == 11) or (flag_maxprice == 12 and flag_minprice == 12) or (flag_maxprice == 13 and flag_minprice == 13) or (flag_maxprice == 14 and flag_minprice == 14) or(flag_maxprice == 15 and flag_minprice == 15) or(flag_maxprice == 16 and flag_minprice == 16) or(flag_maxprice == 17 and flag_minprice == 17) or (flag_maxprice == 18 and flag_minprice == 18) or (flag_maxprice == 19 and flag_minprice == 19) or (flag_maxprice == 20 and flag_minprice == 20) or (flag_maxprice == 21 and flag_minprice == 21) or (flag_maxprice == 22 and flag_minprice == 22) or (flag_maxprice == 23 and flag_minprice == 23) or (flag_maxprice == 24 and flag_minprice == 24):
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

    if (flag_maxprice == 1 and flag_minprice == 1) or (flag_maxprice == 2 and flag_minprice == 2) or(flag_maxprice == 3 and flag_minprice == 3) or(flag_maxprice == 4 and flag_minprice == 4) or(flag_maxprice == 5 and flag_minprice == 5) or (flag_maxprice == 6 and flag_minprice == 6) or (flag_maxprice == 7 and flag_minprice == 7) or (flag_maxprice == 8 and flag_minprice == 8) or (flag_maxprice == 9 and flag_minprice == 9) or (flag_maxprice == 10 and flag_minprice == 10) or (flag_maxprice == 11 and flag_minprice == 11) or (flag_maxprice == 12 and flag_minprice == 12) or (flag_maxprice == 13 and flag_minprice == 13) or (flag_maxprice == 14 and flag_minprice == 14) or(flag_maxprice == 15 and flag_minprice == 15) or(flag_maxprice == 16 and flag_minprice == 16) or(flag_maxprice == 17 and flag_minprice == 17) or (flag_maxprice == 18 and flag_minprice == 18) or (flag_maxprice == 19 and flag_minprice == 19) or (flag_maxprice == 20 and flag_minprice == 20) or (flag_maxprice == 21 and flag_minprice == 21) or (flag_maxprice == 22 and flag_minprice == 22) or (flag_maxprice == 23 and flag_minprice == 23) or (flag_maxprice == 24 and flag_minprice == 24):
        await message.answer('Данные получены! \nПодтвердите выполнение алгоритма', reply_markup=confirm_button)

    else:
        await message.answer('Выберите дальнейшее действие', reply_markup=price_button)

    await state.finish()


  
    

@dp.message_handler(text="Отменить")
async def cancel_start(message: types.Message):
    await message.answer('Хорошо! \nВы будете возвращены в меню', reply_markup=menu_first)



@dp.message_handler(text="Подтвердить")
async def confirm_start(message: types.Message):
    global min_price, max_price, count_pages, pars

    await message.answer('Принято! Начинается обработка...', reply_markup = ReplyKeyboardRemove())

    soup = pars.pages_count(min_price, max_price)

    await message.answer('Код получен!')

    digit_list = get_count_page(soup)

    try:
        digit = ''.join([digit_list[0], digit_list[1]])

    except IndexError:
        digit = digit_list[0]

    count_pages = math.ceil(int(digit) / 28)

    await message.answer(f'В указанном диапазоне найдено {count_pages} страниц.\nПродолжить обработку или прервать выполнение?',
                                                                                        reply_markup = confirm_algorithm_button)


@dp.message_handler(text="Прервать")
async def cancel_alghoritm(message: types.Message):
    await message.answer('Хорошо! \nВы будете возвращены в меню', reply_markup=menu_first)



@dp.message_handler(text="Продолжить обработку")
async def continue_alghoritm(message: types.Message):
    await message.answer('Ok!\nВведите кол-во страниц для парсинга\nМакс. 55', reply_markup = ReplyKeyboardRemove())
    await ParserStates.continue_alghoritm.set()

@dp.message_handler(state = ParserStates.continue_alghoritm)
async def continue_alghoritm(message: types.Message, state = FSMContext):
    global max_price, min_price, pars

    if message.text.isdigit() and int(message.text) <= 55 and int(message.text) > 1:
        answer_count_page = message.text

        await message.answer(f'Примерное время ожидания {0.16 * int(answer_count_page):.2f} мин')

        df_links_flat = pars.links_flat(max_price, min_price, answer_count_page)
        df_links_flat.to_csv('flat_links_one_questions.csv', index = False)

        await message.answer('Файл со ссылками на квартиры создан успешно!\nПродолжаем?', reply_markup = confirm_pars_button)
        await state.finish()

    else:
        await message.answer('Убедитесь, что введено число и оно не превышает 55')
    

@dp.message_handler(text="Остановить машину!")
async def cancel_parser(message: types.Message):
    await message.answer('Хорошо! \nВы будете возвращены в меню', reply_markup=menu_first)
    



    
