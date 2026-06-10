from server.crud import subscription_crud
from server.core import comparison_service, notification_service, id_replace_service
from server.schemas.subscription import SubscriptionData


async def get_all_users_subs_service(db):
    result = await subscription_crud.get_all_subs(db)
    return result


async def update_users_data_service(new_data, db):
    cached_data = await subscription_crud.get_all_subs(db)
    cached_data = [SubscriptionData.model_validate(sub).model_dump() for sub in cached_data]

    diff = await comparison_service.find_diff(cached_data, new_data)

    await subscription_crud.update_subscriptions(db, new_data)

    if diff:
        diff = await id_replace_service.replacer(db, diff)
        await notification_service.notificator(diff)
