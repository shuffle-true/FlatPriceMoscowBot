from aiogram.dispatcher.filters.state import StatesGroup, State

class ParserStates(StatesGroup):
    minprice = State()
    maxprice = State()
    continue_alghoritm = State()
