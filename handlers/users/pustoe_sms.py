from loader import dp
from aiogram import types

@dp.message_handler()
async def get_non_info(message: types.Message):
    await message.answer('Упс! Выбери что нибудь из меню 😌')