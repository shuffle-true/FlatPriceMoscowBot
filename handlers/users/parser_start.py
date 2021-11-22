from loader import dp
from aiogram import types
from aiogram.dispatcher.filters import Command
from .parser import chrome_open

@dp.message_handler(Command("pars"))
async def get(message: types.Message):
    chrome_open()