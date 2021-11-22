from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from .parser import chrome_open
from aiogram.dispatcher import FSMContext
from states import ParserStates
from keyboards.default import price_button
from aiogram.types import ReplyKeyboardRemove 
k=0
l=0

@dp.message_handler(Command("pars"))
async def get_chrome(message: types.Message):
    chrome = chrome_open()
    chrome.minimize_window()
    await message.answer('Драйвер запущен. \nВыберите действие.', reply_markup = price_button)


@dp.message_handler(text="Ввести нижний порог цены")
async def get_min_price(message: types.Message):
    await message.answer('Укажите нижний порог', reply_markup = ReplyKeyboardRemove())
    await ParserStates.minprice.set()

@dp.message_handler(state = ParserStates.minprice)
async  def enter_min_price(message: types.Message,state=FSMContext):
    min_price = message.text
    global l
    l=1
    if k == 1 and l == 1:
        await message.answer('Ввод принят', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Выберите дальнейшее действие', reply_markup=price_button)
    await state.finish()
@dp.message_handler(text="Ввести верхний порог цены")
async def get_max_price(message: types.Message):
    await message.answer('Укажите верхний порог', reply_markup = ReplyKeyboardRemove())
    await ParserStates.maxprice.set()
@dp.message_handler(state = ParserStates.maxprice)
async  def enter_max_price(message: types.Message,state=FSMContext):
    max_price = message.text
    global k
    k=1
    if k == 1 and l == 1:
        await message.answer('Ввод принят', reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer('Выберите дальнейшее действие', reply_markup=price_button)
    await state.finish()

