import httpx
import logging

from bot.data.config import BACKEND_URL, API_COMMANDS


async def send_subscription_to_api(user_id: int, name: str, url: str) -> dict | None:
    payload = {
        "user_id": user_id,
        "name": name,
        "url": url
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{BACKEND_URL}{API_COMMANDS["add_sub"]}", json=payload, timeout=5)
            if response.status_code in (200, 201):
                return response.json()

            elif response.status_code == 422:
                logging.error(f"Bad data from user {response.text}")
                return {"status": "error", "detail": "invalid data"}

            else:
                logging.error(f"Сервер вернул ошибку {response.status_code}: {response.text}")
                return None

        except httpx.ConnectError:
            logging.error(f"Server is dead.......")
            return None
