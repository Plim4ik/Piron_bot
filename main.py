import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Command
from handlers.bot_handlers import cmd_start, process_excel_file, button_handler, cmd_get_minutes
from keyboards.keyboards import callback_data
from config import TOKEN


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(cmd_start, Command('start'))
dp.register_callback_query_handler(cmd_get_minutes, callback_data.filter(command="get_minutes"))
dp.register_callback_query_handler(button_handler, callback_data.filter())




dp.register_message_handler(process_excel_file, content_types=types.ContentTypes.DOCUMENT)

if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)


