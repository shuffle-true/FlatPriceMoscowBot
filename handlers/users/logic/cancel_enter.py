from loader import dp
from aiogram import types
from keyboards.default import menu_first
from aiogram.dispatcher import FSMContext
from states import MenuButton




@dp.message_handler(text="Отменить ввод")
async def get_cancel_enter(message: types.Message):
    await message.answer('Вы вернулись в меню',reply_markup=menu_first)
