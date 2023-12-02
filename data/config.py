from environs import Env

env = Env()
env.read_env() 

BOT_TOKEN = env.str("BOT_TOKEN")

DB_FILE = env.str("DB_FILE")

OPENAI_API_KEY = env.str("OPENAI_API_KEY")