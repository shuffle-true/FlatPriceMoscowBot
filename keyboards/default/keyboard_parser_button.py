from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

price_button = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Ввести нижний порог цены")
        ],
        [
            KeyboardButton(text="Ввести верхний порог цены")
        ],
    ],
    resize_keyboard=True
)


price_button_max = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Указать верхний порог цены")
        ],
    ],
    resize_keyboard=True
)

price_button_min = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Указать нижний порог цены")
        ],
    ],
    resize_keyboard=True
)