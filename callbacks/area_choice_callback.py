from aiogram.filters.callback_data import CallbackData


class AreaChoiceCallback(CallbackData, prefix="area_choice"):
    id: str

