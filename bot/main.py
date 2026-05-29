import asyncio

from aiogram import Bot, Dispatcher

from data.config import TOKEN
from bot.handlers.user_private import user_private_router


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)


async def main():

    await dp.start_polling(bot)

asyncio.run(main())