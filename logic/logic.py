

from data.storage import save_file, get_actual_cache


async def get_users_subscribe_names(user_id):
    users_data = get_actual_cache()
    print(users_data)
    user_subs = users_data.get(str(user_id))
    if user_subs:
        print(user_subs)
        names_list = [i.get("name") for i in user_subs]
        print(names_list)
        return names_list

    return []

async def update_sub_list(user_info):
 pass
