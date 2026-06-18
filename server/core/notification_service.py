import httpx

from response_kit import logger, handle_network_errors
from server.config import BOT_URL

@handle_network_errors
async def notificator(new_data):
    logger.info("Starting function for notify users - <<notificator>>")
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f"{BOT_URL}/notify", json=new_data)
        logger.info("Successfully finished function for notify users - <<notificator>>")

    except Exception as e:
        logger.error(f"Failed to notify users! Function - <<notificator>> | Error - {e}")
        raise e

