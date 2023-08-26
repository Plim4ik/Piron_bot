#bot_handlers.py

import os
from datetime import datetime, timedelta
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from help.minutes_calc import calculate_minutes
from config import EXCEL_FOLDER, ADMINS, ALLOWED_USERS
from keyboards.keyboards import get_start_keyboard, get_back_keyboard

async def button_handler(callback_query: types.CallbackQuery, callback_data: dict):
    user_id = callback_query.from_user.id
    command = callback_data["command"]

    if command == "help":
        await cmd_help(callback_query.message)
    elif command == "update_excel":
        await cmd_update_excel(callback_query.message, user_id)
    elif command == "get_minutes":
        await cmd_get_minutes(callback_query.message, user_id)
    elif command == "start":
        await callback_query.message.edit_text('👋 Привет! Я бот, который поможет вам подсчитать суммарное количество минут.', reply_markup=get_start_keyboard(user_id))

    await callback_query.answer()

async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if user_id not in ALLOWED_USERS and user_id not in ADMINS:
        await message.answer("🔒 Извините, у вас нет доступа к этому боту.")
        return
    await message.bot.send_message(message.chat.id, '👋 Привет! Я бот, который поможет вам подсчитать суммарное количество минут.', reply_markup=get_start_keyboard(user_id))

async def cmd_help(message: types.Message):
    help_msg = "👉 Чтобы получить свои минуты, нужно нажать кнопку [Получить минуты]."
    await message.answer(text=help_msg, reply_markup=get_back_keyboard())
    await message.delete()

async def cmd_update_excel(message: types.Message, user_id: int): 
    if user_id not in ADMINS:
        await message.answer("🔒 Извините, у вас нет доступа к этому функционалу.")
        return
    await message.answer(text='📎 Пожалуйста, отправьте мне файл Excel.', reply_markup=get_back_keyboard())
    await message.delete()



async def cmd_get_minutes(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    # Выполняем расчет минут
    excel_files = [f for f in os.listdir(EXCEL_FOLDER) if f.endswith('.xlsx')]
    excel_files.sort(key=lambda x: os.path.getmtime(os.path.join(EXCEL_FOLDER, x)), reverse=True)
    latest_file = excel_files[0]
    minutes_summary = calculate_minutes(os.path.join(EXCEL_FOLDER, latest_file))

    if user_id in ADMINS:
        # Администраторы получают полный отчет
        await callback_query.message.edit_text(minutes_summary, reply_markup=get_back_keyboard())
    else:
        # Обычные пользователи получают только свои минуты
        user_name = ALLOWED_USERS.get(user_id)
        if user_name:
            user_minutes_line = next((line for line in minutes_summary.split('\n') if user_name in line), None)
            if user_minutes_line:
                await callback_query.message.edit_text(user_minutes_line, reply_markup=get_back_keyboard())
            else:
                await callback_query.message.edit_text(f"❌ Минуты для пользователя {user_name} не найдены.", reply_markup=get_back_keyboard())
        else:
            await callback_query.message.edit_text("🔒 Извините, у вас нет доступа к этому боту.", reply_markup=get_back_keyboard())


async def process_excel_file(message: types.Message):
    if message.from_user.id not in ADMINS:
        await message.answer("🔒 Извините, у вас нет доступа к этому функционалу.")
        return
    if message.document:
        # Путь к файлу внутри папки EXCEL_FOLDER с оригинальным именем файла
        file_name = message.document.file_name
        file_path = os.path.join(EXCEL_FOLDER, file_name)
        await message.document.download(destination_file=file_path)  
        
        # Удаляем сообщение с файлом из чата
        await message.delete()

        # Отправляем сообщение о том, что файл успешно сохранен, и указываем название файла
        success_text = f'✅ Файл успешно сохранен. \nНазвание файла: {file_name}.'
        await message.answer(text=success_text, reply_markup=get_back_keyboard())
        await message.delete()
    else:
        await message.answer(text='📎 Пожалуйста, отправьте мне файл Excel.', reply_markup=get_back_keyboard())
        await message.delete()

