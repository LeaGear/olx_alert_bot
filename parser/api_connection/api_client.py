import httpx

from response_kit import APIResponse, handle_network_errors, log_function, logger
from parser.config import BACKEND_URL, API_REQUESTS

@log_function
@handle_network_errors
async def get_all_users_from_server():
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{API_REQUESTS['get_subs']}"
        response = await client.get(url)
        return APIResponse(status="success", data=response.json())

@handle_network_errors
async def post_updated_data(updated_data):
    logger.info("Starting function - <<post_updated_data>>")
    try:
        payload = APIResponse(status = "success", data=updated_data)

        async with httpx.AsyncClient() as client:
            url = f"{BACKEND_URL}{API_REQUESTS['post_subs']}"
            await client.post(url, json=payload.model_dump())
        logger.info("Function - <<post_updated_data>> finished successfully")
        return APIResponse(status = "success")
    except Exception as e:
        logger.error(f"Function - <<post_updated_data>> failed due to {e}")
