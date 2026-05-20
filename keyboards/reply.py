from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data.config import KEYBOARDS


menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = KEYBOARDS["my_subscribes"]),
            KeyboardButton(text = KEYBOARDS["add_subscribe"])
        ],
        [
            KeyboardButton(text = KEYBOARDS["properties"]),
            KeyboardButton(text = KEYBOARDS["delete_subscribe"])
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Обирай контент!"
)
back_to_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text = KEYBOARDS["menu"])
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Back to Menu!"
)

def get_keyboard(
    *btns: list,
    placeholder: str = None,
    request_contact: int = None,
    request_location: int = None,
    sizes:tuple[int] = (2,)
):
    keyboard = ReplyKeyboardBuilder()
    for btn in btns:
        for index, text in enumerate(btn):
            if request_contact and request_contact == index:
                keyboard.add(KeyboardButton(text = text, request_contact=True))
            elif request_location and request_location == index:
                keyboard.add(KeyboardButton(text = text, request_location=True))
            else:
                keyboard.add(KeyboardButton(text = text))
    return keyboard.adjust(*sizes).as_markup(resize_keyboard  = True, input_field_placeholder = placeholder)