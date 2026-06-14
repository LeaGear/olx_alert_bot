from server.crud import subscription_crud
from server.core import comparison_service, notification_service, id_replace_service


async def get_all_users_subs_service(db):
    result = await subscription_crud.get_all_subs(db)
    return result


async def update_users_data_service(new_data, db):
    await subscription_crud.update_subscriptions(db, new_data)
    new_content = await comparison_service.get_only_new(new_data)
    new_content = await id_replace_service.replacer(db, new_content)
    await notification_service.notificator(new_content)
