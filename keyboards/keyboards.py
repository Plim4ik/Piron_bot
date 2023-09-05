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
    if user_id in ADMINS:
        keyboard_start.add(InlineKeyboardButton("📄 Генерация отчета", callback_data=callback_data.new(command="update_excel")))

    return keyboard_start

def get_back_keyboard():
    keyboard_back = InlineKeyboardMarkup()
    keyboard_back.add(InlineKeyboardButton("◀️ Назад", callback_data=callback_data.new(command="start")))
    return keyboard_back

def get_report_keyboard():
    keyboard_report = InlineKeyboardMarkup()
    keyboard_report.add(InlineKeyboardButton("1️⃣ Первый этап", callback_data=callback_data.new(command="update_excel")))
    keyboard_report.add(InlineKeyboardButton("2️⃣ Второй этап", callback_data=callback_data.new(command="update_excel")))
    return keyboard_report
