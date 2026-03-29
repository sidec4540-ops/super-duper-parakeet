import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import TelegramAPIError

# Читаем токен и ID из ENV
TG_TOKEN = os.getenv("TG_TOKEN")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "").split(",")]
SECRET_KEY = os.getenv("SECRET_KEY")

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot)

# Команда /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("У вас нет доступа")
        return
    await message.reply(f"Бот запущен. Введите пароль:")

# Проверка пароля
@dp.message_handler()
async def check_password(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if message.text.strip() == SECRET_KEY:
        await message.reply("Пароль принят. Бот готов к работе!")
    else:
        await message.reply("Неверный пароль!")

# Авто-перезапуск long polling
async def main():
    while True:
        try:
            await dp.start_polling()
        except TelegramAPIError as e:
            print("Ошибка Telegram API, переподключение...", e)
            await asyncio.sleep(5)
        except Exception as e:
            print("Другая ошибка, переподключение...", e)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())