from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuButton(StatesGroup):
    adress_first = State()
    koord_first = State()
    adress_second = State()
    koord_second = State()
    start_ml = State()
    start_info_for_ml = State()
    start_interactive = State()
    start_info_for_ml_cian = State()
    get_real_target = State()
    set_all_message = State()

