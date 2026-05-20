import asyncio

from aiogram import Bot, Dispatcher

from data.config import TOKEN
from data.storage import check_data_file, caching_users_data
from handlers.user_private import user_private_router


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)


async def main():

    check_data_file() # Call the function to check of the presence of data file, if file not exist - creating new
    await caching_users_data()

    await dp.start_polling(bot)

asyncio.run(main())