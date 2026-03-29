import time
from pip._internal.cli.main import main

# todo убрать когда-то

try:
    import lxml
except ModuleNotFoundError:
    main(["install", "-U", "lxml>=5.3.0"])
except:
    pass
try:
    import bcrypt
except ModuleNotFoundError:
    main(["install", "-U", "bcrypt>=4.2.0"])
except:
    pass
try:
    import socks
except ModuleNotFoundError:
    main(["install", "-U", "pysocks>=1.7.1"])
except:
    pass
import Utils.cardinal_tools
import Utils.config_loader as cfg_loader
from first_setup import first_setup
from colorama import Fore, Style
from Utils.logger import LOGGER_CONFIG
import logging.config
import colorama
import sys
import os
from cardinal import Cardinal
import Utils.exceptions as excs
from locales.localizer import Localizer

VERSION = "0.1.17.6"

Utils.cardinal_tools.set_console_title(f"FunPay Cardinal v{VERSION}")

if getattr(sys, 'frozen', False):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

folders = ["configs", "logs", "storage", "storage/cache", "storage/plugins", "storage/products", "plugins"]
for i in folders:
    if not os.path.exists(i):
        os.makedirs(i)

files = ["configs/auto_delivery.cfg", "configs/auto_response.cfg"]
for i in files:
    if not os.path.exists(i):
        with open(i, "w", encoding="utf-8") as f:
            ...

colorama.init()

logging.config.dictConfig(LOGGER_CONFIG)
logging.raiseExceptions = False
logger = logging.getLogger("main")
logger.debug("------------------------------------------------------------------")

print(f"{Fore.RED}{Style.BRIGHT}v{VERSION}{Style.RESET_ALL}\n")
print(f"{Fore.MAGENTA}{Style.BRIGHT}By {Fore.BLUE}{Style.BRIGHT}Woopertail, @sidor0912{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * GitHub: {Fore.BLUE}{Style.BRIGHT}github.com/sidor0912/FunPayCardinal{Style.RESET_ALL}")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Telegram: {Fore.BLUE}{Style.BRIGHT}t.me/sidor0912")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Новости о обновлениях: {Fore.BLUE}{Style.BRIGHT}t.me/fpc_updates")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Плагины: {Fore.BLUE}{Style.BRIGHT}t.me/fpc_plugins")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Донат: {Fore.BLUE}{Style.BRIGHT}t.me/sidor_donate")
print(f"{Fore.MAGENTA}{Style.BRIGHT} * Telegram-чат: {Fore.BLUE}{Style.BRIGHT}t.me/funpay_cardinal")

# Пропускаем first_setup полностью
if not os.path.exists("configs/_main.cfg"):
    print("Файл configs/_main.cfg не найден, создаю пустой конфиг")

if sys.platform == "linux" and os.getenv('FPC_IS_RUNNIG_AS_SERVICE', '0') == '1':
    import getpass
    pid = str(os.getpid())
    pidFile = open(f"/run/FunPayCardinal/{getpass.getuser()}/FunPayCardinal.pid", "w")
    pidFile.write(pid)
    pidFile.close()
    logger.info(f"PID файл создан, PID процесса: {pid}")

# Загрузка конфига с обработкой ошибок
try:
    logger.info("Загружаю конфиг _main.cfg...")
    MAIN_CFG = cfg_loader.load_main_config("configs/_main.cfg")
except Exception as e:
    logger.error(f"Ошибка загрузки конфига: {e}")
    logger.info("Создаю конфиг по умолчанию...")
    MAIN_CFG = cfg_loader.create_config_obj({})
    MAIN_CFG["Other"] = {"language": "ru"}
    MAIN_CFG["Telegram"] = {"enabled": "1"}
    MAIN_CFG["FunPay"] = {}

try:
    localizer = Localizer(MAIN_CFG.get("Other", {}).get("language", "ru"))
    _ = localizer.translate
except:
    localizer = Localizer("ru")
    _ = localizer.translate

try:
    logger.info("Загружаю конфиг auto_response.cfg...")
    AR_CFG = cfg_loader.load_auto_response_config("configs/auto_response.cfg")
    RAW_AR_CFG = cfg_loader.load_raw_auto_response_config("configs/auto_response.cfg")
except:
    AR_CFG = {}
    RAW_AR_CFG = {}

try:
    logger.info("Загружаю конфиг auto_delivery.cfg...")
    AD_CFG = cfg_loader.load_auto_delivery_config("configs/auto_delivery.cfg")
except:
    AD_CFG = {}

try:
    Cardinal(MAIN_CFG, AD_CFG, AR_CFG, RAW_AR_CFG, VERSION).init().run()
except KeyboardInterrupt:
    logger.info("Завершаю программу...")
    sys.exit()
except Exception as e:
    logger.critical(f"При работе Кардинала произошла ошибка: {e}")
    logger.warning("TRACEBACK", exc_info=True)
    logger.critical("Завершаю программу...")
    time.sleep(5)
    sys.exit()
