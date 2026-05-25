from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import LinkPreviewOptions

from bot.keyboards.reply import menu_keyboard, get_keyboard, back_to_menu_keyboard
from bot.logic.logic import get_users_subscribe_names, get_user_subs
from bot.logic.commands import add_subscribe, delete_subscribe
from bot.data.config import KEYBOARDS
from server.models.subscription import Subscription
from bot.logic.api_client import send_subscription_to_api


user_private_router = Router()


class AddSubscribe(StatesGroup):
    sub_name = State()
    sub_url = State()


class DeleteSubscribe(StatesGroup):
    waiting_for_choice = State()


# START command
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, давай начнем создавать твой рай OLX уведомлений!", reply_markup=menu_keyboard)


# MENU button
@user_private_router.message(F.text == KEYBOARDS["menu"])
async def back_to_menu(message: types.Message, state: FSMContext):

    if await state.get_state(): #If user have active state and in FSM route - clear it
        await state.clear()

    await message.answer("Главное меню: ", reply_markup=menu_keyboard)


# LOOKING user subscribes button
@user_private_router.message(F.text == KEYBOARDS["my_subscribes"])
async def my_subs(message: types.Message):
    user_id = message.from_user.id
    user_subs = await get_user_subs(user_id)
    # print(user_subs)
    if user_subs:
        ans_message = "Список ваших подписок: \n"
        for i in user_subs:
            ans_message += f"{i.get('name')} | {i.get('url')}\n"

        await message.answer(ans_message, link_preview_options=LinkPreviewOptions(is_disabled=True))

    else:
        await message.answer(f"У вас нет ни одной подписки!", reply_markup=menu_keyboard)


# Open FSM route for add new subscribe with name and url
@user_private_router.message(F.text == KEYBOARDS["add_subscribe"])
async def add_subs(message: types.Message, state: FSMContext):
    await message.answer("Введи название подписки: ", reply_markup=back_to_menu_keyboard)
    await state.set_state(AddSubscribe.sub_name)


@user_private_router.message(AddSubscribe.sub_name)
async def add_subscribe_name(message: types.Message, state: FSMContext):
    await message.answer("Имя подписки добавлено! Введите ссылку: ")
    await state.update_data(sub_name=message.text)
    await state.set_state(AddSubscribe.sub_url)


@user_private_router.message(AddSubscribe.sub_url)
async def add_subscribe_url(message: types.Message, state: FSMContext):
    await state.update_data(sub_url=message.text)
    #await message.answer("Ссылка добавлена! Подписка сохранена!")  # Add user subscribes url

    user_data = await state.get_data()  # Get all user data from FSM
    user_id = message.from_user.id  # Getting user ID

    response_status = await send_subscription_to_api(user_id, user_data.get("sub_name"), user_data.get("sub_url"))
    if response_status["detail"] == "add_success":
        await message.answer(f"Добавлена подписка: \n{user_data.get('sub_name')} | {user_data.get('sub_url')}",
                             reply_markup=menu_keyboard)
    elif response_status["detail"] == "invalid_data":
        await message.answer("Подписка не добавлена так как был отправлен неправильный URL", reply_markup=menu_keyboard)
    elif response_status["detail"] == "server_down":
        await message.answer("Напишите додику, что сервак - мертв", reply_markup=menu_keyboard)
    else:
        await message.answer("Разраб обосрался - не воркает", reply_markup = menu_keyboard)

# DELETE subscribe button
@user_private_router.message(F.text == KEYBOARDS["delete_subscribe"])
async def delete_subs(message: types.Message, state: FSMContext):
    user_subs = await get_users_subscribe_names(message.from_user.id)
    if not user_subs:
        await message.answer("У вас еще нет подписок, что-бы что-то удалять!", reply_markup=menu_keyboard)
        await state.clear()
        return

    await state.update_data(user_subs_names=user_subs)
    await state.set_state(DeleteSubscribe.waiting_for_choice)

    await message.answer("Какую подписку хотите удалить?",
                     reply_markup=get_keyboard(user_subs, menu_button=KEYBOARDS["menu"],
                                                   placeholder="Выберите одну из ваших подписок...."))


@user_private_router.message(DeleteSubscribe.waiting_for_choice)
async def del_one_sub(message: types.Message, state: FSMContext):
    subs = await state.get_data()
    if message.text in subs["user_subs_names"]:
        await delete_subscribe(message.from_user.id, message.text)
        await message.answer(f"Подписка {message.text} была удалена!", reply_markup=menu_keyboard)
    else:
        await message.answer(f"Подписки с таким именем не существует!")

    await state.clear()


# PROPERTIES button
@user_private_router.message(F.text == KEYBOARDS["properties"])
async def properties(message: types.Message):
    pass


# OTHER text from USER
@user_private_router.message()
async def input_error(message: types.Message):
    await message.answer("Упс... Что-то пошло не так! Назад в меню...", reply_markup=menu_keyboard)
