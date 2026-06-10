import httpx

from server.config import BOT_URL

async def notificator(new_data):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BOT_URL}/notify", json=new_data)

