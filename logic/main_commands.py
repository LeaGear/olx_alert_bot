
from data.storage import save_file, get_actual_cache
from logic.logic import get_users_subscribe_names


async def my_subscribes():
    pass

async def add_subscribe(user_info):
    actual_cache = get_actual_cache()
    print("Data Cache in add_subscribe", actual_cache)
    print(f"{user_info[0]}")

    if str(user_info[0]) in actual_cache:
        print("Exist route")
        actual_cache[str(user_info[0])].append(user_info[1])
    else:
        print("New route")
        actual_cache[str(user_info[0])] = [user_info[1]]

    #print("Data Cache" , actual_cache)
    await save_file(data = actual_cache)

async def delete_subscribe(user_id, sub_name):
    actual_cache = get_actual_cache()
    users_data = actual_cache.get(str(user_id))
    new_data = [sub for sub in users_data if sub.get("name") != sub_name]
    print("new_data", new_data)
    print(f"actual cache: {actual_cache}")
    actual_cache[str(user_id)] = new_data
    print(f"new new new actual cache: {actual_cache}")
    await save_file(data = actual_cache)


async def properties():
    pass