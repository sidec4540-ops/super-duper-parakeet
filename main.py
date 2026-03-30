import threading
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

from cardinal import Cardinal
from configparser import ConfigParser

# ---------- Настройки ---------- #
TOKEN = "8777560443:AAEwopxAHU6EtrZtJ5PXlVfYlp1wem9OV5c"
ADMIN_ID = 571001160

bot = Bot(token=TOKEN)
dp = Dispatcher()

# ---------- Telegram ---------- #
@dp.message(CommandStart())
async def start(message: types.Message):
    if message.from_user.id == ADMIN_ID:
        await message.answer("✅ Cardinal бот работает")
    else:
        await message.answer("❌ Нет доступа")


async def telegram_bot():
    print("Telegram бот запущен")
    await dp.start_polling(bot)


def run_telegram():
    asyncio.run(telegram_bot())


# ---------- Cardinal ---------- #
def run_cardinal():
    print("Cardinal запускается...")
    
    # Загружаем _main.cfg
    cfg = ConfigParser()
    cfg.read("_main.cfg", encoding="utf-8")

    cardinal = Cardinal(cfg, {}, {}, {}, "0.1.17.6")  # версия
    cardinal.init().run()


# ---------- Запуск ---------- #
if __name__ == "__main__":
    # Telegram в отдельном потоке
    telegram_thread = threading.Thread(target=run_telegram)
    telegram_thread.start()

    # Cardinal
    run_cardinal()