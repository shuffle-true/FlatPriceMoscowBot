from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.default import menu_first, ml_choice
from loader import dp

from tree import TreeRegressor
from tree import TreeRegressorSlow
from ensemble import BaggingTree
from utils_.saving import save_model

import pandas as pd

from aiogram.utils.markdown import link

@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
    """
    Начало работы с ботом.

    Описание команды /start
    """

    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu_first)

@dp.message_handler(text = "Как мною пользоваться?")
async def how_use_me(message: types.Message):
    text = link('Хто я?', 'https://telegra.ph/Kak-menya-yuzat-04-07')
    await message.answer(text,parse_mode="Markdown")


@dp.message_handler(text = "Узнать аренду квартиры! 🤪")
async def choice_ml(message: types.Message):
    await message.answer("*Выберите вариант ввода информации*", parse_mode="Markdown", reply_markup=ml_choice)



##########################################################
###                FITTING - MODEL                     ###
##########################################################
# @dp.message_handler(Command("fit_ml"))
# async def fit_model(message: types.Message):
#     await message.answer("Обучение запущено")
#
#     best_params = {'max_depth': 6, 'min_samples_leaf': 5, 'min_samples_split': 4}
#
#     model = TreeRegressor(**best_params)
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop('price', axis = 1)
#     y = df.price
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/DECISION_TREE_120')
#
#     best_params = {'max_depth': 1, 'min_samples_leaf': 1, 'min_samples_split': 1}
#
#     model = TreeRegressor(**best_params)
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df[df.price < 40000].drop('price', axis=1)
#     y = df[df.price < 40000]['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/DECISION_TREE_40')
#
#     best_params = {'max_depth': 14, 'min_samples_leaf': 3, 'min_samples_split': 1}
#
#     model = TreeRegressorSlow(**best_params)
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/DECISION_TREE_SLOW_120')
#
#     await message.answer("Деревья обучены")
#
#     model = BaggingTree(base_model=TreeRegressorSlow,
#                         n_estimators=10,
#                         max_depth=14,
#                         min_samples_leaf=3,
#                         min_samples_split=1)
#
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/BAGGING_TREE_SLOW_120_10')
#
#     model = BaggingTree(base_model=TreeRegressorSlow,
#                         n_estimators=50,
#                         max_depth=14,
#                         min_samples_leaf=3,
#                         min_samples_split=1)
#
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/BAGGING_TREE_SLOW_120_50')
#
#     model = BaggingTree(base_model=TreeRegressorSlow,
#                         n_estimators=100,
#                         max_depth=14,
#                         min_samples_leaf=3,
#                         min_samples_split=1)
#
#     df = pd.read_csv('Ready_for_fit.csv')
#
#     X = df.drop(['price'], axis=1)
#     y = df['price']
#     model.fit(X, y)
#
#     save_model(model, 'ML_MODEL/BAGGING_TREE_SLOW_120_100')
#
#
#     await message.answer("Модели обучены и готовы к использованию.")

