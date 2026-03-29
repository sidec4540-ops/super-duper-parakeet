import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import TelegramAPIError

# ====== Настройки через ENV ======
TG_TOKEN = os.getenv("TG_TOKEN")
if not TG_TOKEN:
    raise ValueError("TG_TOKEN не задан в ENV")

ADMIN_IDS = os.getenv("ADMIN_IDS", "")
if not ADMIN_IDS:
    raise ValueError("ADMIN_IDS не задан в ENV")
ADMIN_IDS = [int(x.strip()) for x in ADMIN_IDS.split(",")]

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY не задан в ENV")

# ====== Инициализация бота ======
bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

# ====== Команда /start ======
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("У вас нет доступа")
        return
    await message.reply("Бот запущен. Введите пароль:")

# ====== Проверка пароля ======
@dp.message_handler()
async def check_password(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if message.text.strip() == SECRET_KEY:
        await message.reply("Пароль принят. Бот готов к работе!")
    else:
        await message.reply("Неверный пароль!")

# ====== Запуск long polling с авто-перезапуском ======
async def start_bot():
    while True:
        try:
            print("Telegram-бот запущен, ожидаем сообщения...")
            await dp.start_polling()
        except TelegramAPIError as e:
            print("Ошибка Telegram API, переподключение...", e)
            await asyncio.sleep(5)
        except Exception as e:
            print("Другая ошибка Telegram, переподключение...", e)
            await asyncio.sleep(5)

# ====== Точка входа ======
if __name__ == "__main__":
    asyncio.run(start_bot())