from aiogram.filters.callback_data import CallbackData


class SexChoiceCallback(CallbackData, prefix="sex_choice"):
    id: int

