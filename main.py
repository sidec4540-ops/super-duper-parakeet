import os
import sys
import time
import logging.config
import colorama
from colorama import Fore, Style
from configparser import ConfigParser
from Utils.logger import LOGGER_CONFIG
import Utils.cardinal_tools
from cardinal import Cardinal
from locales.localizer import Localizer
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils.exceptions import TelegramAPIError

# ==================== Настройки ====================
VERSION = "0.1.17.6"
Utils.cardinal_tools.set_console_title(f"FunPay Cardinal v{VERSION}")

# Рабочая директория
if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

# Создаём папки
folders = ["configs", "logs", "storage", "storage/cache", "storage/plugins", "storage/products", "plugins"]
for i in folders:
    if not os.path.exists(i):
        os.makedirs(i)

# Логирование
colorama.init()
logging.config.dictConfig(LOGGER_CONFIG)
logging.raiseExceptions = False
logger = logging.getLogger("main")

print(f"{Fore.RED}{Style.BRIGHT}v{VERSION}{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT}By Woopertail, @sidor0912{Style.RESET_ALL}")

# ==================== Конфиги ====================
MAIN_CFG = ConfigParser(delimiters=(":",), interpolation=None)
MAIN_CFG.optionxform = str

MAIN_CFG["Telegram"] = {
    "enabled": "1",
    "token": os.getenv("TG_TOKEN", "8777560443:AAEwopxAHU6EtrZtJ5PXlVfYlp1wem9OV5c"),
    "user_id": os.getenv("ADMIN_IDS", "571001160"),
    "secretKeyHash": os.getenv("SECRET_KEY", "MyPassword123"),
    "blockLogin": "0",
    "proxy": ""
}

# Здесь остальные конфиги оставляем как есть
# (FunPay, Proxy, Other, BlockList, NewMessageView, Greetings, OrderConfirm, ReviewReply)
# Для экономии места пропустим их в этом примере, они остаются без изменений

AR_CFG = ConfigParser(delimiters=(":",), interpolation=None)
AR_CFG.optionxform = str
AD_CFG = ConfigParser(delimiters=(":",), interpolation=None)
AD_CFG.optionxform = str
RAW_AR_CFG = {}

localizer = Localizer("ru")
_ = localizer.translate

logger.info("Запуск Cardinal и Telegram‑бота...")
print("Бот запускается...")

# ==================== Telegram‑бот ====================
TG_TOKEN = MAIN_CFG["Telegram"]["token"]
ADMIN_IDS = [int(x) for x in MAIN_CFG["Telegram"]["user_id"].split(",")]
SECRET_KEY = MAIN_CFG["Telegram"]["secretKeyHash"]

telegram_bot = Bot(token=TG_TOKEN)
dp = Dispatcher(telegram_bot)

@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        await message.reply("У вас нет доступа")
        return
    await message.reply("Бот запущен. Введите пароль:")

@dp.message_handler()
async def check_password(message: types.Message):
    if message.from_user.id not in ADMIN_IDS:
        return
    if message.text.strip() == SECRET_KEY:
        await message.reply("Пароль принят. Бот готов к работе!")
    else:
        await message.reply("Неверный пароль!")

async def start_telegram_bot():
    while True:
        try:
            await dp.start_polling()
        except TelegramAPIError as e:
            print("Ошибка Telegram API, переподключение...", e)
            await asyncio.sleep(5)
        except Exception as e:
            print("Другая ошибка Telegram, переподключение...", e)
            await asyncio.sleep(5)

# ==================== Запуск Cardinal + Telegram ====================
async def main():
    # Старт Telegram асинхронно
    asyncio.create_task(start_telegram_bot())
    
    # Старт Cardinal
    try:
        Cardinal(MAIN_CFG, AD_CFG, AR_CFG, RAW_AR_CFG, VERSION).init().run()
    except KeyboardInterrupt:
        logger.info("Завершаю программу...")
        sys.exit()
    except Exception as e:
        logger.critical(f"Ошибка Cardinal: {e}")
        import traceback
        traceback.print_exc()
        time.sleep(5)
        sys.exit()

if __name__ == "__main__":
    asyncio.run(main())