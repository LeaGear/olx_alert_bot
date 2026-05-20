
from data.storage import save_file, get_actual_cache



async def my_subscribes():
    pass

async def add_subscribe(user_info):
    actual_cache = get_actual_cache()
    #print("Data Cache in add_subscribe", actual_cache)
    #print(f"{user_info[0]}")

    if user_info[0] in actual_cache:
        #print("Exist route")
        actual_cache[user_info[0]].append(user_info[1])
    else:
        #print("New route")
        actual_cache[user_info[0]] = [user_info[1]]

    #print("Data Cache" , actual_cache)
    await save_file(data = actual_cache)

async def delete_subscribe():
    pass

async def properties():
    pass