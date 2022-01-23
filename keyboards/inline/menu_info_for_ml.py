from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_dates import choice_callback

zalog = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="1 месяц",
                                                          callback_data=choice_callback.new(name="zalog", count="1")),
                                     InlineKeyboardButton(text="2+ месяца",
                                                          callback_data=choice_callback.new(name="zalog", count="2")),
                                     InlineKeyboardButton(text="Без залога",
                                                          callback_data=choice_callback.new(name="zalog", count="0"))
                                 ]
                             ],
                             resize_keyboard=True
                             )

comissions = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="0 - 20%",
                                                          callback_data=choice_callback.new(name="comissions", count="10")),
                                     InlineKeyboardButton(text="20 - 50%",
                                                          callback_data=choice_callback.new(name="comissions", count="50"))
                                 ],
                                 [
                                     InlineKeyboardButton(text="50 - 80%",
                                                          callback_data=choice_callback.new(name="comissions",
                                                                                            count="70")),
                                     InlineKeyboardButton(text="80 - 100%",
                                                          callback_data=choice_callback.new(name="comissions",
                                                                                            count="100"))
                                 ]
                             ],
                             resize_keyboard=True
                             )


predoplata = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="1 месяц",
                                                          callback_data=choice_callback.new(name="prepay", count="1")),
                                     InlineKeyboardButton(text="2+ месяца",
                                                          callback_data=choice_callback.new(name="prepay", count="2")),
                                     InlineKeyboardButton(text="Без предоплаты",
                                                          callback_data=choice_callback.new(name="prepay", count="0"))
                                 ]
                             ],
                             resize_keyboard=True
                             )
