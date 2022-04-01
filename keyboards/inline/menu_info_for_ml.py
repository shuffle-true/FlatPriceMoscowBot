from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_dates import choice_callback

zalog = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="1 месяц",
                                                          callback_data=choice_callback.new(name="zalog", count=1)),
                                     InlineKeyboardButton(text="2+ месяца",
                                                          callback_data=choice_callback.new(name="zalog", count=2)),
                                     InlineKeyboardButton(text="Без залога",
                                                          callback_data=choice_callback.new(name="zalog", count=3))
                                 ]
                             ],
                             resize_keyboard=True
                             )

comissions = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="0 - 20%",
                                                          callback_data=choice_callback.new(name="comissions", count=10)),
                                     InlineKeyboardButton(text="20 - 50%",
                                                          callback_data=choice_callback.new(name="comissions", count=50))
                                 ],
                                 [
                                     InlineKeyboardButton(text="50 - 80%",
                                                          callback_data=choice_callback.new(name="comissions",
                                                                                            count=70)),
                                     InlineKeyboardButton(text="80 - 100%",
                                                          callback_data=choice_callback.new(name="comissions",
                                                                                            count=100))
                                 ]
                             ],
                             resize_keyboard=True
                             )


predoplata = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="1 месяц",
                                                          callback_data=choice_callback.new(name="prepay", count=1)),
                                     InlineKeyboardButton(text="2+ месяца",
                                                          callback_data=choice_callback.new(name="prepay", count=2)),
                                     InlineKeyboardButton(text="Без предоплаты",
                                                          callback_data=choice_callback.new(name="prepay", count=0))
                                 ]
                             ],
                             resize_keyboard=True
                             )

lift = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="1",
                                                          callback_data=choice_callback.new(name="lift", count=1)),
                                     InlineKeyboardButton(text="2",
                                                          callback_data=choice_callback.new(name="lift", count=2))
                                 ],
                                 [
                                     InlineKeyboardButton(text="2+",
                                                          callback_data=choice_callback.new(name="lift", count=4))
                                 ]
                             ],
                             resize_keyboard=True
                             )

count_room = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="1",
                                                          callback_data=choice_callback.new(name="room", count=1)),
                                     InlineKeyboardButton(text="2",
                                                          callback_data=choice_callback.new(name="room", count=2)),
                                     InlineKeyboardButton(text="3",
                                                          callback_data=choice_callback.new(name="room", count=3))
                                 ],
                                 [
                                     InlineKeyboardButton(text="4+",
                                                          callback_data=choice_callback.new(name="room", count=4))
                                 ]
                             ],
                             resize_keyboard=True
                             )

type_of_room = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Квартира",
                                                          callback_data=choice_callback.new(name="type_of_room", count=0)),
                                 ],
                                 [

                                     InlineKeyboardButton(text="Студия",
                                                          callback_data=choice_callback.new(name="type_of_room", count=1)),
                                     InlineKeyboardButton(text="Апартаменты",
                                                          callback_data=choice_callback.new(name="type_of_room", count=2))
                                 ]
                             ],
                             resize_keyboard=True
                             )

type_of_repair = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Дизайнерский",
                                                          callback_data=choice_callback.new(name="type_of_repair", count=2)),
                                     InlineKeyboardButton(text="Евроремонт",
                                                          callback_data=choice_callback.new(name="type_of_repair", count=1))
                                 ],
                                 [

                                     InlineKeyboardButton(text="Косметический",
                                                          callback_data=choice_callback.new(name="type_of_repair", count=0)),
                                 ]
                             ],
                             resize_keyboard=True
                             )



view_window = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="На улицу",
                                                          callback_data=choice_callback.new(name="view_window", count=1)),
                                     InlineKeyboardButton(text="Во двор",
                                                          callback_data=choice_callback.new(name="view_window", count=0))
                                 ],
                                 [

                                     InlineKeyboardButton(text="На улицу и во двор",
                                                          callback_data=choice_callback.new(name="view_window", count=2))
                                 ]
                             ],
                             resize_keyboard=True
                             )

type_of_house = InlineKeyboardMarkup(row_width=3,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Блочный",
                                                          callback_data=choice_callback.new(name="type_of_house",
                                                                                            count=0)),
                                     InlineKeyboardButton(text="Кирпичный",
                                                          callback_data=choice_callback.new(name="type_of_house",
                                                                                            count=1))
                                 ],
                                 [
                                     InlineKeyboardButton(text="Панельный",
                                                          callback_data=choice_callback.new(name="type_of_house", count=3)),
                                 ],
                                 [
                                     InlineKeyboardButton(text="Монолитный",
                                                          callback_data=choice_callback.new(name="type_of_house",
                                                                                            count=6)),
                                     InlineKeyboardButton(text="Монолитно кирпичный",
                                                          callback_data=choice_callback.new(name="type_of_house",
                                                                                            count=7))
                                 ],
                             ],
                             resize_keyboard=True
                             )

type_of_parking = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Наземная",
                                                          callback_data=choice_callback.new(name="type_of_parking", count=0)),
                                     InlineKeyboardButton(text="Подземная",
                                                          callback_data=choice_callback.new(name="type_of_parking",
                                                                                            count=1))
                                 ],
                                 [
                                     InlineKeyboardButton(text="Открытая",
                                                          callback_data=choice_callback.new(name="type_of_parking",
                                                                                            count=2)),
                                 ]
                             ],
                             resize_keyboard=True
                             )

mebel_room = InlineKeyboardMarkup(row_width=2,
                             inline_keyboard=[
                                 [
                                     InlineKeyboardButton(text="Мебель в есть",
                                                          callback_data=choice_callback.new(name="mebel_room", count=0)),
                                     InlineKeyboardButton(text="Отсутствует",
                                                          callback_data=choice_callback.new(name="mebel_room", count=1)),
                                 ],
                             ],
                             resize_keyboard=True
                             )

mebel_kitchen = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard = [
                                                  [
                                                      InlineKeyboardButton(text="В наличии",
                                                                           callback_data=choice_callback.new(name="mebel_kitchen", count=0)),
                                                      InlineKeyboardButton(text="Отсутствует",
                                                                           callback_data=choice_callback.new(name="mebel_kitchen", count=1)),
                                                  ],
                                              ],
                            resize_keyboard = True
                            )

balcony = InlineKeyboardMarkup(row_width=2,
                            inline_keyboard = [
                                                  [
                                                      InlineKeyboardButton(text="Да, балкон есть",
                                                                           callback_data=choice_callback.new(name="balcony", count=0)),
                                                      InlineKeyboardButton(text="Отсутствует",
                                                                           callback_data=choice_callback.new(name="balcony", count=1)),
                                                  ],
                                              ],
                            resize_keyboard = True
                            )




