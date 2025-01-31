import asyncio
from aiogram.methods import DeleteWebhook
from app.bot import bot, dp
from app.handlers import router
from database.database import sql

async def main():
    dp.include_router(router)

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print("Start")
        sql()
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")