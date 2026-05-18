from aiogram import F, types, Router
from aiogram.filters import CommandStart

from keyboards.reply import start_keyboard
from logic.main_commands import my_subscribes, add_subscribe, delete_subscribe, properties
user_private_router = Router()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hi hi hi", reply_markup = start_keyboard)


@user_private_router.message(F.text == "🗒 Мои подписки!")
async def my_subs(message : types.Message):
    await my_subscribes()
    pass

@user_private_router.message(F.text == "🟢 Добавить подписку!")
async def add_subs(message : types.Message):
    await add_subscribe()
    pass

@user_private_router.message(F.text == "🔴 Удалить подписку")
async def delete_subs(message : types.Message):
    await delete_subscribe()
    pass

@user_private_router.message(F.text == "⚙️ Настройки")
async def properties(message: types.Message):
    await properties()
    pass

@user_private_router.message()
async def input_error(message: types.Message):
    await message.answer("Something went wrong!", reply_markup = start_keyboard)
