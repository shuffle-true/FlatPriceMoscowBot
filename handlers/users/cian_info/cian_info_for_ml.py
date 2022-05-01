import time

import pandas as pd
from aiogram import types

from handlers.users.ml.lol import answer_ml, random_fact
from loader import dp
from states import MenuButton
from aiogram.dispatcher import FSMContext
import numpy as np
from keyboards.default import menu_first
from aiogram.types import ReplyKeyboardRemove

from handlers.users.parser.parser import Parser
from handlers.users.cian_info.df_append_cian import df_append
from handlers.users.dataframe.dataframe_preprocessing import Preprocessing


from handlers.users.ml.ml_predict import predict
from data.all_config import columns

from numpy import random as rnd


@dp.message_handler(text = "Ссылка на Циан")
async def link_cian(message: types.Message):
    await message.answer("*Я не рекомендую использовать этот способ оценки. Лучше всего вбивать параметры руками.*\n\n"
"Пришли мне ссылку на квартиру с ЦИАНа", reply_markup = ReplyKeyboardRemove(), parse_mode="Markdown")
    await MenuButton.start_info_for_ml_cian.set()

@dp.message_handler(state=MenuButton.start_info_for_ml_cian)
async def get_link_cian(message: types.Message, state: FSMContext):
    flag = True
    await message.answer("Начал собирать информацию о квартире....")
    pars = Parser()
    try:
        soup = pars.get_flat(np.array([str(message.text)]), 0)



        df = pd.DataFrame()
        try:
            df = df_append(soup, df)
        except AttributeError:
            await message.answer("*Произошла непредвиденная ошибка. Поправим в следующих версиях.*", parse_mode="Markdown", reply_markup=menu_first)
            await state.finish()
            return

        await message.answer("*Информация собрана.*\n\nНачинаю подготовку данных для анализа", parse_mode="Markdown")

        df.to_csv('USER_REQUEST/{}.csv'.format(message.from_user.id), index=False)
        df.to_excel('USER_REQUEST/{}.xlsx'.format(message.from_user.id), index=False)




        preprop = Preprocessing()
        df = preprop.run_preprocessing_script(False, 'USER_REQUEST/{}.csv'.format(message.from_user.id), modified=False)


        df = df.drop(['district', 'coord', 'lat', 'lon', ], axis = 1)

        try:
            df['price'] = df['price'][0].replace(' ', '')
        except IndexError:
            await message.answer("*К сожалению, данного района нет в моей базе данных и я не смогу сделать предсказание.\n\n"
    "Но я исправлюсь, обещаю..)*", parse_mode="Markdown", reply_markup=menu_first)
            flag = False
            await state.finish()

        if flag:
            df = df.astype(float)
            df['metro_time_log'] = np.log(df['metro_time'])
            df['square_log'] = df['square']
            df['floor_log'] = np.log(df['floor'])
            df['azdist_log'] = np.log(df['dist_kreml'] * df['azimut'])
            df['mpa'] = (df['mpa'] / 40) * df['square_log']

            df = df[columns]

            df.to_csv('USER_REQUEST/{}.csv'.format(message.from_user.id), index=False)
            df.to_excel('USER_REQUEST/{}.xlsx'.format(message.from_user.id), index=False)

            await message.answer("*Начинаю предсказание...*", parse_mode="Markdown")

            ans = predict(message.from_user.id)

            await message.answer(f"{answer_ml[rnd.randint(0, len(answer_ml))]}\n\n*{random_fact[rnd.randint(0, len(random_fact))]}*", parse_mode="Markdown")

            time.sleep(4)
            await message.answer(f"*Аренда за эту квартиру составляет {round(np.mean(ans), 0)} руб.\n"
                                 f"Я уверен в прогнозе на {round(100 - (np.var(ans) ** 0.5 / np.mean(ans)), 0)} %.*", parse_mode='Markdown',
                                 reply_markup=menu_first)

            await state.finish()
    except:
        await message.answer("*Распознана попытка взлома. Попытка неудачная. Я продолжаю работать.*", parse_mode="Markdown")


# f"*Decision Tree O(1): {ans[0]} руб.\n"
# f"Decision Tree O(N  log N): {ans[1]} руб.\n"
# f"Bagging Tree O(10N log N): {ans[2]} руб.\n"
# f"Bagging Tree O(50N log N): {ans[3]} руб.\n"
# f"Bagging Tree O(100N log N): {ans[4]} руб.\n"
# f"Mean for all model: {round(np.mean(ans), 0)} руб.\n"
# f"Standart Deviation: {round(np.var(ans) ** 0.5, 0)} руб.*"

