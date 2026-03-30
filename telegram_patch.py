import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

# Получаем переменные окружения Railway
TOKEN = os.getenv("TG_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_IDS", "0"))
PASSWORD = os.getenv("PASSWORD", "12345")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Используем state через словарь для отслеживания авторизации
user_authorized = {}

@dp.message(Command(commands=["start"]))
async def start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Нет доступа")
        return
    user_authorized[message.from_user.id] = False
    await message.answer("Введите пароль:")

@dp.message()
async def password_check(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    if not user_authorized.get(message.from_user.id, False):
        if message.text == PASSWORD:
            user_authorized[message.from_user.id] = True
            await message.answer("✅ Бот активирован")
        else:
            await message.answer("❌ Неверный пароль")
    else:
        await message.answer("Бот уже работает ✅")

async def main():
    print("🚀 Telegram бот запущен")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())