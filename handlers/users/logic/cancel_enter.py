from loader import dp
from aiogram import types
from keyboards.default import menu_first





@dp.message_handler(text="Отменить ввод")
async def get_cancel_enter(message: types.Message):
    """
    Возвращает в меню при нажатии "Отменить ввод"
    """
    await message.answer('Вы вернулись в меню',reply_markup=menu_first)
