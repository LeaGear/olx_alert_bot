import httpx

from response_kit import log_function
from server.config import BOT_URL

@log_function
async def notificator(new_data):
    async with httpx.AsyncClient() as client:
        await client.post(f"{BOT_URL}/notify", json=new_data)
