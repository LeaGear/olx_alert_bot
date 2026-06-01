import asyncio

from parser.logic.parser_logic import parser
from parser.api_connection.api_client import get_all_users_from_server, post_updated_data

async def main_func_parser():

    actual_data = await get_all_users_from_server()
    print("ACTUAL DATA __________", actual_data)
    updated_data = parser(actual_data)
    print("UPDATED DATA __________", updated_data)
    await post_updated_data(updated_data)


async def main():
    print("Starting parser")
    await main_func_parser()
    print("Finish parser")

asyncio.run(main())
