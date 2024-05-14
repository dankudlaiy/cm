from aiogram.fsm.state import State, StatesGroup


class States(StatesGroup):
    area_choice = State()
    sex_choice = State()
    age_choice = State()
