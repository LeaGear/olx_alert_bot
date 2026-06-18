import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from response_kit import log_function,logger

from parser.logic.parser_logic import parser
from parser.api_connection.api_client import get_all_users_from_server, post_updated_data
from parser.config import REFRESH_INTERVAL

scheduler = AsyncIOScheduler()

@log_function
async def main_func_parser():
    actual_data = await get_all_users_from_server()
    updated_data = parser(actual_data.data)
    await post_updated_data(updated_data)

@log_function
async def main():
    scheduler.add_job(main_func_parser, "interval", minutes=REFRESH_INTERVAL, next_run_time=datetime.now())
    scheduler.start()

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down parser...")
        scheduler.shutdown()


asyncio.run(main())
