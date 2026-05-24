from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from bot.data.config import KEYBOARDS

menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARDS["my_subscribes"]),
            KeyboardButton(text=KEYBOARDS["add_subscribe"])
        ],
        [
            KeyboardButton(text=KEYBOARDS["properties"]),
            KeyboardButton(text=KEYBOARDS["delete_subscribe"])
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Обирай контент!"
)
back_to_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=KEYBOARDS["menu"])
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Back to Menu!"
)


def get_keyboard(
        *btns: list,
        menu_button: str = None,
        placeholder: str = None,
        request_contact: int = None,
        request_location: int = None,
        sizes: tuple[int] = (2,)
):
    keyboard = ReplyKeyboardBuilder()
    total_main_buttons = 0

    for btn in btns:
        for index, text in enumerate(btn):
            total_main_buttons += 1
            if request_contact and request_contact == index:
                keyboard.add(KeyboardButton(text=text, request_contact=True))
            elif request_location and request_location == index:
                keyboard.add(KeyboardButton(text=text, request_location=True))
            else:
                keyboard.add(KeyboardButton(text=text))
    if menu_button:
        keyboard.add(KeyboardButton(text=menu_button))
        buttons_per_row = sizes[0]
        full_rows = total_main_buttons // buttons_per_row

        if total_main_buttons % buttons_per_row == 0:
            final_size = (buttons_per_row,) * full_rows + (1,)
        else:
            final_size = (buttons_per_row,) * full_rows + (1,) + (1,)
    else:
        final_size = sizes
    return keyboard.adjust(*final_size).as_markup(resize_keyboard=True, input_field_placeholder=placeholder)
