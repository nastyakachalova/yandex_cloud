from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu_keyboard():
    kb_list = [
        [KeyboardButton(text="Выбрать город"), KeyboardButton(text="Тестовое сообщение")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder='Выберите вариант из меню :)'
    )
    return keyboard

Приложение 3
Файл earthquake.py
# earthquake.py

import aiohttp
from geopy.geocoders import Nominatim


# Получение координат города
async def get_coordinates(city: str):
    geolocator = Nominatim(user_agent="earthquake_bot")
    location = geolocator.geocode(city)

    if location:
        return location.latitude, location.longitude
    return None, None


# Получение данных о землетрясениях
async def get_earthquake_data(lat: float, lon: float):
    url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&latitude={lat}&longitude={lon}&maxradius=500"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
