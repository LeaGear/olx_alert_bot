from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

start_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text = "🗒 Мои подписки!"),
            KeyboardButton(text = "🟢 Добавить подписку!")
        ],
        [
            KeyboardButton(text = "⚙️ Настройки"),
            KeyboardButton(text = "🔴 Удалить подписку")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Обирай контент!"
)
menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text = "Back to Menu!")
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder="Back to Menu!"
)