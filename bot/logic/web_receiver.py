from aiohttp import web
from response_kit import log_function

@log_function
def create_app(bot):

    @log_function
    async def handle_notify(request):
        data = await request.json()
        for obj in data:
            sub_name = obj.get('name')
            last_announcement = obj.get('content')[0]
            all_new_announs = len(obj.get("content"))
            message = build_message(sub_name, last_announcement, all_new_announs)
            await bot.send_message(chat_id=obj.get("user_id"), text=message)

        return web.Response(text="ok")

    @log_function
    def build_message(sub_name, last_announcement, all_announs) -> str:
        return (
            f"🔔 Новое в подписке '{sub_name}':\n"
            f"Всего новых -> {all_announs}\n"
            f"Самое новое :\n"
            f"{last_announcement.get('name')}\n"
            f"Цена: {last_announcement.get('price')}\n"
            f"Ссылка: {last_announcement.get('link')}"
        )

    app = web.Application()
    app.router.add_post("/notify", handle_notify)
    return app
