from bot.storage import get_actual_cache


async def get_users_subscribe_names(user_id):
    users_data = get_actual_cache()
    user_subs = users_data.get(str(user_id))
    if user_subs:
        names_list = [i.get("name") for i in user_subs]
        return names_list

    return []


async def get_user_subs(user_id):
    users_data = get_actual_cache()
    user_subs = users_data.get(str(user_id))

    if user_subs:
        subs_list = [i for i in user_subs]
        return subs_list

    return []


async def update_sub_list(user_info):
    pass
