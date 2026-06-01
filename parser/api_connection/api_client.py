import httpx

from my_shared import APIResponse, Detail, handle_network_errors
from parser.config import BACKEND_URL, API_REQUESTS




@handle_network_errors
async def get_all_users_from_server():
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{API_REQUESTS['get_subs']}"
