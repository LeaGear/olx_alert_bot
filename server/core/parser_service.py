import logging
from server.crud import subscription_crud

async def get_all_users_subs_service(db):
    result = await subscription_crud.get_all_subs(db)
    logging.error(f"RESULT in SERVICE __________ {result} AND type ----------")
    return result