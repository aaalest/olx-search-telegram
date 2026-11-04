from aiogram.filters.callback_data import CallbackData


class MenuNavCallback(CallbackData, prefix="menu"):
    action: str
    param: str = ""