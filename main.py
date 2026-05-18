import asyncio


from aiogram import Bot, Dispatcher

from data.config import TOKEN
from handlers.user_private import user_private_router


bot = Bot(token=TOKEN)
dp = Dispatcher()

dp.include_router(user_private_router)

#def chek():
#    book = {
#        12312 : {"game" : "https/game.com", "board_game": "https/board_game.com"},
#        "12676890" : {"gamiks" : "https/gamikse.com", "steam": "https/steam.com"}
#    }
#    for i in book.get(12312).keys():
#        print(i)
#    print(book.get(12312).values())

async def main():
    await dp.start_polling(bot)

asyncio.run(main())