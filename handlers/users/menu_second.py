from loader import dp
from aiogram import types
from keyboards.default import menu_second


@dp.message_handler(text="В меню")
async def get_adress_second(message: types.Message):
    await message.answer('Вы вернулись в меню',reply_markup=menu_second)