from aiogram import types
from aiogram.dispatcher.filters import Command
from keyboards.default import menu_first
from loader import dp

from tree import TreeRegressor
from tree import TreeRegressorSlow
from utils_.saving import save_model

import pandas as pd

@dp.message_handler(Command("start"))
async def show_menu(message: types.Message):
    """
    Начало работы с ботом.

    Описание команды /start
    """

    await message.answer(f"Привет, {message.from_user.full_name}!", reply_markup=menu_first)


@dp.message_handler(Command("fit_ml"))
async def fit_model(message: types.Message):
    best_params = {'max_depth': 6, 'min_samples_leaf': 5, 'min_samples_split': 4}

    model = TreeRegressor(**best_params)
    df = pd.read_csv('Ready_for_fit.csv')

    X = df.drop('price', axis = 1)
    y = df.price
    model.fit(X, y)

    save_model(model, 'DECISION_TREE_120')

    best_params = {'max_depth': 1, 'min_samples_leaf': 1, 'min_samples_split': 1}

    model = TreeRegressor(**best_params)
    df = pd.read_csv('Ready_for_fit.csv')

    X = df[df.price < 40000].drop('price', axis=1)
    y = df[df.price < 40000]['price']
    model.fit(X, y)

    save_model(model, 'DECISION_TREE_40')

    best_params = {'max_depth': 14, 'min_samples_leaf': 3, 'min_samples_split': 1}

    model = TreeRegressorSlow(**best_params)
    df = pd.read_csv('Ready_for_fit.csv')

    X = df.drop(['price'], axis=1)
    y = df['price']
    model.fit(X, y)

    save_model(model, 'DECISION_TREE_SLOW_120')

    await message.answer("Модели обучены и готовы к использованию.")

