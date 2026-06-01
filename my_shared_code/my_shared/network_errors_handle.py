import functools
import httpx

from .api_response import APIResponse, Detail

def handle_network_errors(func):  # Handler for servers error
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.TimeoutException) as e:
            return APIResponse(status =  "error", detail =  Detail.SERVER_DOWN)

    return wrapper