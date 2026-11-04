from aiogram.utils.keyboard import InlineKeyboardBuilder
from olx_search_telegram.callbacks import MenuNavCallback


def back_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="⬅️ Back", callback_data=MenuNavCallback(action="main"))
    return builder.as_markup()
