from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from olx_search_telegram.keyboards import (
    MenuNavCallback,
    get_back_keyboard,
    get_language_keyboard,
    get_main_menu_keyboard,
)


router = Router()


@router.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "<b>OLX Search Bot</b>\nSelect an option below:",
        reply_markup=get_main_menu_keyboard(),
        parse_mode="HTML"
    )


@router.callback_query(MenuNavCallback.filter())
async def handle_navigation(callback: CallbackQuery, callback_data: MenuNavCallback):
    await callback.answer()

    if callback_data.action == "main":
        text = "<b>OLX Search Bot</b>\nSelect an option below:"
        markup = get_main_menu_keyboard()
    elif callback_data.action == "search":
        text = "<b>Search Configuration</b>\nEnter search query or target URL:"
        markup = get_back_keyboard()
    elif callback_data.action == "lang":
        if callback_data.param:
            # TODO: Persist language selection to PostgreSQL here
            text = f"Language updated to: <b>{callback_data.param.upper()}</b>"
        else:
            text = "<b>Select Language:</b>"
        markup = get_language_keyboard()
    else:
        return

    # In-place message modification
    if callback.message.text != text or callback.message.reply_markup != markup:
        try:
            await callback.message.edit_text(text=text, reply_markup=markup, parse_mode="HTML")
        except Exception:
            pass  # Suppress 'message is not modified' error
