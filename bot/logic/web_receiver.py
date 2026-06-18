from aiohttp import web
from response_kit import log_function

from bot.keyboards.inline import olx_link_inline


@log_function
def create_app(bot):

    @log_function
    async def handle_notify(request):
        data = await request.json()
        for obj in data:
            user_id = obj.get("user_id")

            sub_name = obj.get('name')
            last_announcement = obj.get('content')[0]

            message = build_message(sub_name, last_announcement)

            photo_url = last_announcement.get('image')
            ad_link = last_announcement.get('link')

            inline_keyboard = await olx_link_inline(ad_link)

            try:
                if photo_url and photo_url != "No Photo":
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=photo_url,
                        caption=message,
                        reply_markup=inline_keyboard,
                        parse_mode="Markdown"
                    )
                else:
                    await bot.send_message(
                        chat_id=user_id,
                        text=message,
                        reply_markup=inline_keyboard,
                        parse_mode="Markdown"
                    )
            except Exception as e:
                print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

        return web.Response(text="ok")

    @log_function
    def build_message(sub_name, last_announcement) -> str:
        return (
            f"🔔 **Новое в подписке:** '{sub_name} 🔔'\n\n"
            f"📌 {last_announcement.get('name')} 📌\n\n"
            f"💰 {last_announcement.get('price')} 💰\n\n"
            f"📍 {last_announcement.get('location', 'Не указана')} 📍"
        )

    app = web.Application()
    app.router.add_post("/notify", handle_notify)
    return app
