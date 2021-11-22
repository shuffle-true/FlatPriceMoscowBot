import time
from loader import dp
from aiogram import types
from keyboards.default import menu_coord_second, menu_back_from_random_state, menu_second
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from states import MenuButton
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter



def coord_process(lat, lon):
    reverse_geocoder = RateLimiter(Nominatim(user_agent='tutorial').reverse, min_delay_seconds=1)
    coord_process = reverse_geocoder((lat, lon))
    return coord_process




@dp.message_handler(text="Обратное геокодирование")
async def get_reverse_geocode_first(message: types.Message):
    await message.answer("Введите координаты в формате: \n XX.xxxxxx YY.yyyyyy", reply_markup=ReplyKeyboardRemove())
    await MenuButton.koord_first.set()


@dp.message_handler(state=[MenuButton.koord_first, MenuButton.koord_second])
async def get_reverse_geocode_process(message: types.Message,state: FSMContext):
    if ' ' in message.text:
        coord = message.text
        lat = coord.split(' ')[0]
        lon = coord.split(' ')[1]
        if len(lat) == 9 and len(lon) == 9 and lat[2] == '.' and lon[2] == '.':
            await message.answer('По заданным координатам найден объект:')
            time.sleep(1)
            await message.answer(f'{coord_process(lat, lon)}', reply_markup = menu_coord_second)
            await state.finish()
        else:
            if message.text == 'Отменить ввод':
                await state.finish()
                await message.answer('Вы вернулись в меню',reply_markup=menu_second)
            else:
                await message.answer('Координаты не обнаружены. Повторите ввод', reply_markup = menu_back_from_random_state)
    else:
        if message.text == 'Отменить ввод':
            await state.finish()
            await message.answer('Вы вернулись в меню',reply_markup=menu_second)
        else:
            await message.answer('Проверьте формат ввода', reply_markup = menu_back_from_random_state)

@dp.message_handler(text="Ввести еще одни координаты")
async def get_reverse_geocode_first(message: types.Message):
    await message.answer("Введите координаты",
                         reply_markup=ReplyKeyboardRemove())
    await MenuButton.koord_second.set()