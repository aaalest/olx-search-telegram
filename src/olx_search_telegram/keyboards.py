from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenuNavCallback(CallbackData, prefix="menu"):
    action: str
    param: str = ""


def get_main_menu_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🔍 Search", callback_data=MenuNavCallback(action="search"))
    builder.button(text="🌐 Language", callback_data=MenuNavCallback(action="lang"))
    builder.adjust(2)
    return builder.as_markup()


def get_language_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🇬🇧 English", callback_data=MenuNavCallback(action="lang", param="en"))
    builder.button(text="🇵🇱 Polski", callback_data=MenuNavCallback(action="lang", param="pl"))
    builder.button(text="🇺🇦 Українська", callback_data=MenuNavCallback(action="lang", param="uk"))
    builder.button(text="⬅️ Back", callback_data=MenuNavCallback(action="main"))
    builder.adjust(1, 1, 1, 1)
    return builder.as_markup()


def get_back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Back", callback_data=MenuNavCallback(action="main"))
    return builder.as_markup()
