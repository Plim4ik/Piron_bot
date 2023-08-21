from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config import ADMINS

callback_data = CallbackData("action", "command")

def get_start_keyboard(user_id):
    keyboard_start = InlineKeyboardMarkup()
    keyboard_start.add(InlineKeyboardButton("🆘 Помощь", callback_data=callback_data.new(command="help")))
    keyboard_start.add(InlineKeyboardButton("🕓 Получить минуты", callback_data=callback_data.new(command="get_minutes")))
    if user_id in ADMINS:
        keyboard_start.add(InlineKeyboardButton("♻️ Обновить Excel", callback_data=callback_data.new(command="update_excel")))
    return keyboard_start

def get_back_keyboard():
    keyboard_back = InlineKeyboardMarkup()
    keyboard_back.add(InlineKeyboardButton("◀️ Назад", callback_data=callback_data.new(command="start")))
    return keyboard_back
