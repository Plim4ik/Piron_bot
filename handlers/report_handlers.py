import os
from aiogram import types
from config import EXCEL_REPORTS_FOLDER
from middlewares.report_processing import handle_report_file
from keyboards import get_back_keyboard


async def cmd_create_report(message: types.Message):
    user_id: int = message.from_user.id
    if user_id not in OWNERS:
        try:
            await message.message.answer("Извините, у вас нет доступа к этой функции.")
        except AttributeError:
            await message.answer("Извините, у вас нет доступа к этой функции.")
            await message.message.delete()
        return

    try:
        await message.answer("Пожалуйста, загрузите файл .xlsx для формирования отчета.", reply_markup=get_back_keyboard())
    except AttributeError:
            await message.message.answer("Пожалуйста, загрузите файл .xlsx для формирования отчета.", reply_markup=get_back_keyboard())
            await message.message.delete()


# Добавляем новую функцию для обработки файла отчета
async def process_report_file(message: types.Message):
    user_id = message.from_user.id
    if user_id not in OWNERS or message.document is None:
        return

    # Сохраняем файл
    file_path = os.path.join(EXCEL_REPORTS_FOLDER, message.document.file_name)
    await message.document.download(destination_file=file_path)

    try:
        await message.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id, text="Файл успешно загружен. Пожалуйста, подождите...", reply_markup=get_back_keyboard())
    except AttributeError:
        await message.message.answer("Файл успешно загружен. Пожалуйста, подождите...", reply_markup=get_back_keyboard())
        await message.message.delete()

    output_file_path = handle_report_file(file_path) 
    
    await message.delete()

    # Отправляем файл пользователю
    with open(output_file_path, "rb") as file:
        try:
            await message.answer_document(file, caption="Отчет для первого этапа сформирован.")
        except AttributeError:
            await message.message.answer(file, caption = "Отчет для первого этапа сформирован.")
            await message.message.delete()
