import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import bot_token, admins
from db import init_db
from user import router as user_router
from karzinka import k_router
from db import test_products
test_products()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher()

dp.include_router(user_router)
dp.include_router(k_router)

async def main():
    init_db()
    for admin in admins:
        try:
            await bot.send_message(chat_id=admin, text="Bot ishga tushdi ✅")
        except:
            pass
    print("🤖 Bot pollingni boshladi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())





