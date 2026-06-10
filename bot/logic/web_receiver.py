from aiohttp import web


def create_app(bot):
    async def handle_notify(request):
        data = await request.json()
        print(data)
        for obj in data:
            message = build_message(obj)
            await bot.send_message(chat_id=obj.get("id"), text=message)

        return web.Response(text="ok")

    def build_message(item: dict) -> str:
        return (
            f"🔔 Новое в подписке:\n"
            f"{item.get('name')}\n"
            f"Цена: {item.get('price')}\n"
            f"Ссылка: {item.get('link')}"
        )

    app = web.Application()
    app.router.add_post("/notify", handle_notify)
    return app