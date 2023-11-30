from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config
from utils.db_api import BotDb, DbUsers

bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

bot_db = BotDb(config.DB_FILE)
db_users = DbUsers()