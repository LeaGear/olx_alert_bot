from dataclasses import asdict

from bot.logic.storage import save_file, get_actual_cache


async def my_subscribes():
    pass


async def add_subscribe(user_info):
    actual_cache = get_actual_cache()

    user_data = asdict(user_info)
    user_data.pop("user_id")
    if str(user_info.user_id) in actual_cache:
        actual_cache[str(user_info.user_id)].append(user_data)
    else:
        actual_cache[str(user_info.user_id)] = [user_data]

    await save_file(data=actual_cache)


async def delete_subscribe(user_id, sub_name):
    actual_cache = get_actual_cache()
    users_data = actual_cache.get(str(user_id), [])
    if not users_data:
        return
    new_data = [sub for sub in users_data if sub.get("name") != sub_name]
    actual_cache[str(user_id)] = new_data
    await save_file(data=actual_cache)


async def properties():
    pass
