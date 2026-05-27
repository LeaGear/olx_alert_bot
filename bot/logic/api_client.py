import httpx
import logging
import functools

from bot.data.config import BACKEND_URL, API_COMMANDS


def handle_network_errors(func):  # Handler for servers error
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
            return {"status": "error", "detail": "unknow error"}


@handle_network_errors
async def get_user_subs(user_id: int) -> list[dict] | None:
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{API_COMMANDS['get_user_subs'].format(user_id)}"
        response = await client.get(url, timeout=5)
        if response:
            return response.json()
        else:
            return None


@handle_network_errors
async def delete_user_sub(user_id: int, sub_name: str) -> dict:
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{API_COMMANDS['delete_sub'].format(user_id, sub_name)}"
        print(url)
        response = await client.delete(url, timeout=5)
        if response.status_code == 204:
            logging.warning(f"Sub was deleted!")
            return {"status": "success", "detail": "sub_deleted"}
        elif response.status_code == 404:
            logging.error(f"Sub was not found!")
            return {"status": "error", "detail": "sub_not_found"}
        else:
            logging.error(f"Unknow problem {response.status_code}")
            return {"status": "error", "detail": "unknow error"}
