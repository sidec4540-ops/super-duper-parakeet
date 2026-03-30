import os
import asyncio
from aiogram import Bot, Dispatcher, types

# Берём данные из Railway Variables
TOKEN = os.getenv("TG_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_IDS", "0"))
PASSWORD = os.getenv("PASSWORD", "12345")

bot = Bot(token=TOKEN)
dp = Dispatcher()

authorized = False

@dp.message(commands=["start"])
async def start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("Нет доступа")
        return
    await message.answer("Введите пароль")

@dp.message()
async def password_check(message: types.Message):
    global authorized

    if message.from_user.id != ADMIN_ID:
        return

    if not authorized:
        if message.text == PASSWORD:
            authorized = True
            await message.answer("✅ Бот активирован")
        else:
            await message.answer("❌ Неверный пароль")
    else:
        await message.answer("Бот работает")

async def main():
    print("Telegram бот запущен")
    await dp.start_polling(bot)

asyncio.run(main())