from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu_first = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text = "Узнать аренду квартиры! 🤪")
        ],
        # [
        #     KeyboardButton(text="Интерактивчик 😐")
        # ],
        # [
        #     KeyboardButton(text="Как мною пользоваться?")
        # ],
    ],
    resize_keyboard=True
)

ml_choice = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text = "Самостоятельный ввод")
        ],
        [
            KeyboardButton(text="Ссылка на Циан")
        ]
    ],
    resize_keyboard=True
)



menu_adress_second = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Ввести еще один адрес 🏠")
        ],
        [
            KeyboardButton(text="В меню")
        ],
    ],
    resize_keyboard=True
)
menu_second = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Ввести адрес 🏠")
        ],
        [
            KeyboardButton(text="Обратное геокодирование")
        ],
    ],
    resize_keyboard=True
)
menu_coord_second = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Ввести еще одни координаты")
        ],
        [
            KeyboardButton(text="В меню")
        ],
    ],
    resize_keyboard=True
)

menu_back_from_random_state = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text="Отменить ввод")
        ],
    ],
    resize_keyboard=True
)

menu_confirm_start_ml = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text = "Продолжить")
        ],    
        [
            KeyboardButton(text = "Отменить ввод")    
        ],
    ],
    resize_keyboard=True
    )

menu_confirm = ReplyKeyboardMarkup(
    [
        [
            KeyboardButton(text = "ЖОПА")
        ],
    ],
    resize_keyboard=True
)

