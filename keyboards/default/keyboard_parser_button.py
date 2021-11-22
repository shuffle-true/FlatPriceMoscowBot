from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

price_button = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Ввести нижний порог цены"),
            KeyboardButton(text="Ввести верхний порог цены"),
        ],
    ],
    resize_keyboard=True
)