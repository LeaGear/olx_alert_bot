
from server.crud import user_crud


async def replacer(db, data):
    users_ids = await user_crud.get_users_ids(db)

    for obj in data:
        obj["user_id"] = users_ids[obj["user_id"]]

    return data