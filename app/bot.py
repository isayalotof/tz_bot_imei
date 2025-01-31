from aiogram import Bot, Dispatcher
from config.config import tg_token

bot = Bot(token=tg_token)
dp = Dispatcher()