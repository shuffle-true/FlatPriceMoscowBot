from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.default import menu_first
from loader import dp



@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
    """
    Начало работы с ботом.

    Описание команды /start
    """
    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu_first)