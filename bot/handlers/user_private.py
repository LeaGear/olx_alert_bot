from aiogram import F, types, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import LinkPreviewOptions

from bot.keyboards.reply import menu_keyboard, get_keyboard, back_to_menu_keyboard
from bot.data.config import KEYBOARDS
from bot.logic.api_client import send_subscription_to_api, get_user_subs, delete_user_sub
from bot.schemas.api_response import Detail

user_private_router = Router()


class AddSubscribe(StatesGroup):
    sub_name = State()
    sub_url = State()


class DeleteSubscribe(StatesGroup):
    waiting_for_choice = State()


async def send_main_menu(message: types.Message, state: FSMContext = None, text: str = "Главное меню: "):
    if state and await state.get_state():  # If user have active state and in FSM route - clear it
        await state.clear()

    await message.answer(text, reply_markup=menu_keyboard)


# START command
@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, давай начнем создавать твой рай OLX уведомлений!", reply_markup=menu_keyboard)


# MENU button
@user_private_router.message(F.text == KEYBOARDS["menu"])
async def back_to_menu(message: types.Message, state: FSMContext):
    await send_main_menu(message, state)


# LOOKING user subscribes button
@user_private_router.message(F.text == KEYBOARDS["my_subscribes"])
async def my_subs(message: types.Message):
    sub_list = await get_user_subs(message.from_user.id)

    if not sub_list.ok:
        if sub_list.detail == Detail.NOT_FOUND:
            await message.answer("У вас нет ни одной подписки!")
        else:
            await message.answer("Проблемы с сервером!")
        await send_main_menu(message)
        return

    subs_message = "Ваши подписки: \n"
    for sub in sub_list.data:
        subs_message += f"{sub.get('name')} | {sub.get('url')}\n"
    await message.answer(subs_message, link_preview_options=LinkPreviewOptions(is_disabled=True))
    await send_main_menu(message)


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

    user_data = await state.get_data()  # Get all user data from FSM
    user_telegram_id = message.from_user.id  # Getting user ID
    response_status = await send_subscription_to_api(user_telegram_id, user_data.get("sub_name"),
                                                     user_data.get("sub_url"))

    if response_status.ok:
        await message.answer(f"Добавлена подписка: \n{user_data.get('sub_name')} | {user_data.get('sub_url')}")

    else:
        if response_status.detail == Detail.INVALID_DATA:
            await message.answer("Подписка не добавлена так как был отправлен неправильный URL")
        elif response_status.detail == Detail.SERVER_DOWN:
            await message.answer("Напишите додику, что сервак - мертв")
        else:
            await message.answer("Разраб обосрался - не воркает")

    await send_main_menu(message, state)


# DELETE subscribe button
@user_private_router.message(F.text == KEYBOARDS["delete_subscribe"])
async def delete_sub(message: types.Message, state: FSMContext):
    server_user_sub_names = await get_user_subs(message.from_user.id)

    if server_user_sub_names.ok:
        user_subs = [sub.get("name") for sub in server_user_sub_names.data]

        await state.set_state(DeleteSubscribe.waiting_for_choice)

        await message.answer("Какую подписку хотите удалить?",
                             reply_markup=get_keyboard(user_subs, menu_button=KEYBOARDS["menu"],
                                                       placeholder="Выберите одну из ваших подписок...."))
    else:
        if server_user_sub_names.detail == Detail.NOT_FOUND:
            await message.answer("У вас еще нет подписок, что-бы что-то удалять!")
        else:
            await message.answer("Проблемы с сервером!")
        await send_main_menu(message, state)
        return


@user_private_router.message(DeleteSubscribe.waiting_for_choice)
async def del_one_sub(message: types.Message, state: FSMContext):
    user_telegram_id = message.from_user.id
    server_response = await delete_user_sub(user_telegram_id, message.text)

    if server_response.ok:
        await message.answer(f"Подписка {message.text} была удалена!")
    else:
        if server_response.detail == Detail.NOT_FOUND:
            await message.answer(f"Подписки с таким именем не существует!")
        else:
            await message.answer("Неизвестная ошибка, попробуйте еще раз!")

    await send_main_menu(message, state)


# PROPERTIES button
@user_private_router.message(F.text == KEYBOARDS["properties"])
async def properties(message: types.Message):
    pass


# OTHER text from USER
@user_private_router.message()
async def input_error(message: types.Message):
    await message.answer("Упс... Что-то пошло не так! Назад в меню...", reply_markup=menu_keyboard)
