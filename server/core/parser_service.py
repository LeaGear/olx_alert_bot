from server.crud import subscription_crud
from server.core import comparison_service, notification_service


async def get_all_users_subs_service(db):
    result = await subscription_crud.get_all_subs(db)
    return result


async def update_users_data_service(new_data, db):
    cached_data = await subscription_crud.get_all_subs(db)

    await subscription_crud.update_subscriptions(db, new_data)

    diff = await comparison_service.find_diff(cached_data, new_data)

    if diff:
        await notification_service.notificator(diff)
