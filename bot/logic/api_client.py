import httpx
import logging
import functools

from bot.data.config import BACKEND_URL, API_COMMANDS


#Handler for servers error
def handle_network_errors(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.TimeoutException) as e:
            logging.error(f"Network error in function - '{func.__name__}()': {e}")
            return {"status": "error", "detail": "server_down"}

    return wrapper


@handle_network_errors
async def send_subscription_to_api(user_id: int, name: str, url: str) -> dict | None:
    payload = {
        "user_id": user_id,
        "name": name,
        "url": url
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}{API_COMMANDS['add_sub']}", json=payload, timeout=5)

        if response.status_code in (200, 201):
            logging.warning(f"All good server response - {response.json()}")
            return response.json()

        elif response.status_code == 422:
            logging.error(f"Bad data from user {response.text}")
            return {"status": "error", "detail": "invalid_data"}

        else:
            logging.error(f"Сервер вернул ошибку {response.status_code}: {response.text}")
            return {"status" : "error", "detail": "unknow error"}
