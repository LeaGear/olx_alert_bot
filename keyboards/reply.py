from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.config import KEYBOARDS


start_keyboard = ReplyKeyboardMarkup(
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
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text = KEYBOARDS["menu"])
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Back to Menu!"
)