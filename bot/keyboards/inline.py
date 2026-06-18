from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def olx_link_inline(link):
    inline_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🌐 Перейти на OLX",
                    url=link
                )
            ]
        ]
    )
    return inline_keyboard
