import aiosqlite

# Получение подключения к базе данных
async def get_db_connection():
    db = await aiosqlite.connect('earthquakes.db')  # Открываем существующую базу данных
    return db

# Сохранение города пользователя в базе данных
async def save_user_city(db, user_id: int, city: str, lat: float, lon: float):
    async with db:
        await db.execute('''INSERT OR REPLACE INTO users (user_id, city, lat, lon) 
                            VALUES (?, ?, ?, ?)''', (user_id, city, lat, lon))
        await db.commit()

# Получение города пользователя из базы данных
async def get_user_city(db, user_id: int):
    async with db:
        cursor = await db.execute('''SELECT city, lat, lon FROM users WHERE user_id = ?''', (user_id,))
        row = await cursor.fetchone()
        return row
