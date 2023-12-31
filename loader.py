from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from data import config
from utils.db_api import BotDb, DbUsers
from keyboards import Keyboards


bot = Bot(token=config.BOT_TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

OPENAI_API_KEY = config.OPENAI_API_KEY

bot_db = BotDb(config.DB_FILE)
db_users = DbUsers()

keyboards = Keyboards()