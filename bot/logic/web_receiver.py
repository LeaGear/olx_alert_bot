from aiohttp import web


def create_app(bot):
    async def handle_notify(request):
        data = await request.json()
        print(data)
        for obj in data:
            sub_name = obj.get('name')
            last_announcement = obj.get('content')[0]
            all_new_announs = len(obj.get("content")) + 1
            message = build_message(sub_name, last_announcement, all_new_announs)
            print(f"Sending message to user - {obj.get('user_id')}---------->>>>>>: \n{message}\n")
            await bot.send_message(chat_id=obj.get("user_id"), text=message)
            print(f"Message '{message}' sent complete \n{'---' * 20}")


        return web.Response(text="ok")

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