import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeDefault
from aiogram.filters import Command, StateFilter
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from config import API_TOKEN  # Ваш API токен
from handlers import cmd_start, cmd_city, process_city  # Импортируем обработчики
from middleware import DBMiddleware  # Импортируем middleware

# Основная функция
async def main():
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    # Добавляем middleware для работы с БД
    dp.middleware.setup(DBMiddleware())  # Подключаем middleware

    # Устанавливаем команды
    commands = [
        BotCommand(command='start', description='Знакомство с Ботом'),
        BotCommand(command='city', description='Выбрать город для мониторинга землетрясений'),
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())

    # Регистрируем обработчики
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_city, Command("city"))
    dp.message.register(process_city, StateFilter("city"))

    try:
        # Запускаем бота
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()

# Запуск приложения
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())

