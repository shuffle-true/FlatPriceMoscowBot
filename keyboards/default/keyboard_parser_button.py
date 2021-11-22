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

confirm_button = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Подтвердить"),
        ],
        [
            KeyboardButton(text="Отменить"),
        ],
    ],
    resize_keyboard=True
)

confirm_algorithm_button = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Продолжить обработку"),
        ],
        [
            KeyboardButton(text="Прервать"),
        ],
    ],
    resize_keyboard=True
)

confirm_pars_button = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Начать парсинг квартир"),
        ],
        [
            KeyboardButton(text="Остановить машину!"),
        ],
    ],
    resize_keyboard=True
)