from aiogram.dispatcher.filters.state import StatesGroup, State


class UserRegistrationStates(StatesGroup):
    enter_one_win_id = State()
