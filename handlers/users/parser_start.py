from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from .parser import chrome_open
from aiogram.dispatcher import FSMContext
from states import ParserStates
from keyboards.default import price_button, price_button_max, price_button_min
from aiogram.types import ReplyKeyboardRemove 

@dp.message_handler(Command("pars"))
async def get_chrome(message: types.Message):
    chrome = chrome_open()
    chrome.minimize_window()
    await message.answer('Драйвер запущен. \nВыберите действие.', reply_markup = price_button)
