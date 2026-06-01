from server.crud import subscription_crud

async def get_all_users_subs_service(db):
    result = await subscription_crud.get_all_subs(db)
    return result

async def update_users_data(new_data, db):
    await subscription_crud.update_subscriptions(db, new_data)
