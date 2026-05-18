from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from keyboards.reply import start_keyboard, menu_keyboard
from logic.logic import get_users_subscribe_names, update_sub_list
from logic.main_commands import my_subscribes, add_subscribe, delete_subscribe, properties
user_private_router = Router()

class AddSubscribe(StatesGroup):
    sub_name = State()
    sub_url = State()

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hi hi hi", reply_markup = start_keyboard)


@user_private_router.message(F.text == "🗒 Мои подписки!")
async def my_subs(message : types.Message):
    await my_subscribes()
    pass


#Open FSM route for add new subscribe with name and url
@user_private_router.message(F.text == "🟢 Добавить подписку!")
async def add_subs(message : types.Message, state: FSMContext):
    #await add_subscribe()
    await message.answer("Введи название подписки: ", reply_markup = menu_keyboard)
    await state.set_state(AddSubscribe.sub_name)

@user_private_router.message(AddSubscribe.sub_name)
async def add_subscribe_name(message: types.Message, state: FSMContext):
    user_subname_list = await get_users_subscribe_names(message.from_user.id)
    if message.text in user_subname_list:
        await message.answer("Subscribe name must be unique! Try another!")
        return
    else:
        await message.answer("Name added!")
        await state.update_data(sub_name=message.text)
        await state.set_state(AddSubscribe.sub_url)

@user_private_router.message(AddSubscribe.sub_url)
async def add_subscribe_url(message: types.Message, state: FSMContext):
    await state.update_data(sub_url=message.text)
    await message.answer("Subscribe url added!")

@user_private_router.message(AddSubscribe.sub_url)
async def add_path_end(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    user_id = message.from_user.id
    user_dict = {user_id : {user_data.get("sub_name") : user_data.get("sub_url")}}
    await update_sub_list(user_dict)
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
