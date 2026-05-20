from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State


from keyboards.reply import start_keyboard, menu_keyboard
from logic.logic import get_users_subscribe_names
from logic.main_commands import my_subscribes, add_subscribe, delete_subscribe, properties
from data.config import KEYBOARDS


user_private_router = Router()

class AddSubscribe(StatesGroup):
    sub_name = State()
    sub_url = State()

#START command
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Hi hi hi", reply_markup = start_keyboard)

#MENU button
@user_private_router.message(F.text == KEYBOARDS["menu"])
async def back_to_menu(message: types.Message):
    await message.answer("Main menu: ", reply_markup = start_keyboard)

#LOOKING user subscribes button
@user_private_router.message(F.text == KEYBOARDS["my_subscribes"])
async def my_subs(message : types.Message):
    await my_subscribes()
    pass


#Open FSM route for add new subscribe with name and url
@user_private_router.message(F.text == KEYBOARDS["add_subscribe"])
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
    await message.answer("Subscribe url added!", reply_markup = start_keyboard) #Add user subscribes url

    #await message.answer("Now save your data")
    user_data = await state.get_data() #Get all user data from FSM
    user_id = message.from_user.id #Getting user ID
    user_new_sub = [user_id, {"name" : user_data.get("sub_name"), "url" : user_data.get("sub_url")}] #Create list with user data
    #print(f"user new info  -- -- - {user_new_sub}")
    #print(f"data cache while add user - - - - {await get_actual_cache()}")
    await add_subscribe(user_new_sub)



#DELETE subscribe button
@user_private_router.message(F.text == KEYBOARDS["delete_subscribe"])
async def delete_subs(message : types.Message):
    user_subs = await get_users_subscribe_names(message.from_user.id)
    if not user_subs:
        await message.answer("You haven`t subscribes", reply_markup = menu_keyboard)
    else:
        await message.answer("Choose subscribe for delete!",reply_markup = menu_keyboard)
        await delete_subscribe()

#PROPERTIES button
@user_private_router.message(F.text == KEYBOARDS["properties"])
async def properties(message: types.Message):
    await properties()
    pass

#OTHER text from USER
@user_private_router.message()
async def input_error(message: types.Message):
    await message.answer("Something went wrong!", reply_markup = start_keyboard)
