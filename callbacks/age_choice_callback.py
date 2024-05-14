from aiogram.filters.callback_data import CallbackData


class AgeChoiceCallback(CallbackData, prefix="age_choice"):
    id: str

