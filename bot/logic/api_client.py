from xmlrpc.client import SERVER_ERROR

import httpx
import logging
import functools

from bot.data.config import BACKEND_URL, API_COMMANDS
from bot.schemas.api_response import APIResponse, Detail

def handle_network_errors(func):  # Handler for servers error
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.TimeoutException) as e:
            logging.error(f"Network error in function - '{func.__name__}()': {e}")
            return APIResponse(status =  "error", detail =  Detail.SERVER_DOWN)

    return wrapper


@handle_network_errors
async def send_subscription_to_api(user_id: int, name: str, url: str) -> APIResponse[None]:
    payload = {
        "telegram_id": user_id,
        "name": name,
        "url": url
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BACKEND_URL}{API_COMMANDS['add_sub']}", json=payload, timeout=5)

        if response.status_code in (200, 201):
            logging.warning(f"All good! Server response")
            return APIResponse(status = "success", detail = Detail.SUB_ADDED)

        elif response.status_code == 422:
            logging.error(f"Bad data from user {response.text}")
            return APIResponse(status = "error", detail = Detail.INVALID_DATA)

        else:
            logging.error(f"Сервер вернул ошибку {response.status_code}: {response.text}")
            return APIResponse(status = "error", detail = Detail.UNKNOWN)


@handle_network_errors
async def get_user_subs(user_id: int) -> APIResponse[list[dict]]:
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{API_COMMANDS['get_user_subs'].format(user_id)}"
        response = await client.get(url, timeout=5)

        if response.status_code == 200:
            return APIResponse(status = "success", detail = "list_of_user_subs", data = response.json())
        elif response.status_code == 404:
            return APIResponse(status = "error", detail = Detail.SUBS_NOT_FOUND)
        else:
            return APIResponse(status = "error", detail = Detail.UNKNOWN)


@handle_network_errors
async def delete_user_sub(user_id: int, sub_name: str) -> APIResponse[None]:
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{API_COMMANDS['delete_sub'].format(user_id, sub_name)}"
        response = await client.delete(url, timeout=5)

        if response.status_code == 204:
            logging.warning(f"Sub was deleted!")
            return APIResponse(status = "success", detail = Detail.SUB_DELETED)
        elif response.status_code == 404:
            logging.error(f"Sub was not found!")
            return APIResponse(status = "error", detail = Detail.SUBS_NOT_FOUND)
        else:
            logging.error(f"Unknow problem {response.status_code}")
            return APIResponse(status = "error", detail = Detail.UNKNOWN)
