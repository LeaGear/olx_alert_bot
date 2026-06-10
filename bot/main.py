import asyncio

from aiogram import Bot, Dispatcher
from aiohttp import web

from data.config import TOKEN
from bot.handlers.user_private import user_private_router
from logic.web_receiver import create_app

bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)


async def main():
    # Запускаем aiohttp сервер
    app = create_app(bot)  # создаём приложение передавая bot
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8001)
    await site.start()

    # Запускаем aiogram polling
    await dp.start_polling(bot)


asyncio.run(main())
