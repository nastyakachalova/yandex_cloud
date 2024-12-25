import aiosqlite
from aiogram.types import Message
from aiogram import BaseMiddleware
from typing import Dict, Any, Callable, Awaitable  # Добавьте Awaitable и другие типы

from database import get_db_connection


class DBMiddleware(BaseMiddleware):
    def __init__(self):
        super().__init__()

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],  # Добавлен Awaitable
            event: Message,
            data: Dict[str, Any]  # Добавлен Dict
    ) -> Any:
        # Открываем соединение с базой данных
        db_connection = await get_db_connection()
        # Сохраняем соединение в data
        data['db_connection'] = db_connection

        try:
            # Передаем обработчику событие и данные (в том числе соединение с БД)
            return await handler(event, data)
        finally:
            # Закрываем соединение с БД
            await db_connection.close()

