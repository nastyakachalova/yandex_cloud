from aiogram.fsm.context import FSMContext
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from typing import Dict  # Добавлен импорт Dict
from database import get_user_city, save_user_city  # Функции для работы с БД
from earthquake import get_earthquake_data, get_coordinates  # Функции для работы с данными о землетрясениях

async def cmd_start(message: Message, state: FSMContext, data: Dict[str, Any]):
    db_connection = data.get('db_connection')  # Получаем соединение с БД из data
    user_city_data = await get_user_city(db_connection, message.from_user.id)

    if user_city_data:
        city, lat, lon = user_city_data
        await message.answer(f"Привет, {message.from_user.first_name}!\n\n"
                             f"Ты ранее выбрал город {city}. Сейчас я могу отслеживать землетрясения для этого города.\n\n"
                             "Если хочешь выбрать другой город, используй команду /city.")
        earthquake_data = await get_earthquake_data(lat, lon)
        if earthquake_data:
            await message.answer(f"Землетрясения в городе {city}:\n{earthquake_data}")
        else:
            await message.answer(f"Не удалось найти данные о землетрясениях для города {city}.")
    else:
        await message.answer(f"Привет, {message.from_user.first_name}!\n\n"
                             "Ты еще не выбрал город. Пожалуйста, введи название города для отслеживания землетрясений.")

    await state.set_state('choose_city')

async def cmd_city(message: Message, state: FSMContext):
    await message.answer("Введите город для мониторинга землетрясений.")
    await state.set_state('city')

# Обработчик ввода города
async def process_city(message: Message, state: FSMContext, data: Dict[str, Any]):
    db_connection = data.get('db_connection')  # Получаем соединение с БД из data
    city = message.text.strip()

    # Получаем координаты города
    latitude, longitude = await get_coordinates(city)

    if latitude and longitude:
        # Сохраняем город и координаты в базе данных
        await save_user_city(db_connection, message.from_user.id, city, latitude, longitude)
        await message.answer(f"Город {city} сохранен. Теперь я буду уведомлять тебя о землетрясениях в этом городе.")
    else:
        await message.answer(f"Не удалось найти координаты для города {city}. Попробуйте снова.")

    await state.set_state('choose_city')
