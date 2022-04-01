from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_dates import matlab_img

type_of_graph = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text="Scatter Plot",
                                                                  callback_data=matlab_img.new(name="type_of_graph",
                                                                                                    count=0)),
                                             InlineKeyboardButton(text="Bar",
                                                                  callback_data=matlab_img.new(name="type_of_graph",
                                                                                                    count=1))
                                         ]
                                     ],
                                     resize_keyboard=True
                                     )

OX = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text="Square",
                                                                  callback_data=matlab_img.new(name="OX",
                                                                                                    count=0)),
                                             InlineKeyboardButton(text="Floor",
                                                                  callback_data=matlab_img.new(name="OX",
                                                                                                    count=1))
                                         ],
                                         [
                                             InlineKeyboardButton(text="Price",
                                                                  callback_data=matlab_img.new(name="OX",
                                                                                               count=2)),
                                         ]
                                     ],
                                     resize_keyboard=True
                                     )

OY = InlineKeyboardMarkup(row_width=2,
                                     inline_keyboard=[
                                         [
                                             InlineKeyboardButton(text="Metro Time",
                                                                  callback_data=matlab_img.new(name="OY",
                                                                                                    count=0)),
                                         ]
                                     ],
                                     resize_keyboard=True
                                     )

