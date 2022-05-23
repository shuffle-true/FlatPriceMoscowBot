import logging

from aiogram import Dispatcher

from data.config import admins

from data.all_config import TOKEN

async def on_startup_notify(dp: Dispatcher):
    for admin in admins:
        try:
            await dp.bot.send_message(admin,"Приветствую, Повелитель!")

        except Exception as err:
            logging.exception(err)

def check_():
    # if TOKEN == "2145614320:AAEEkcgJRryvRVPhbVUdOWPAvM7iZwAV718":
    #     raise AttributeError(
    #         "Необходимо изменить токен бота. Укажите его в директории программы ../data/all_config.py\n"
    #                          "Указать в режиме для чтения!"
    #     )

    if len(admins) == 0:
        raise ValueError(
            "Не указан ID админа бота. Укажите его в директории программы ../data/config.py --- admins"
        )