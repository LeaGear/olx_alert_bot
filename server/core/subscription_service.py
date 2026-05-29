import logging

from server.crud import user_crud, subscription_crud




async def add_subscription_service(db, telegram_id : int, sub_name : str, sub_url : str):
    user_db_id = await user_crud.get_db_user_id(db, telegram_id)
    if not user_db_id:
        new_user = await user_crud.create_user(db, telegram_id)
        user_db_id = new_user.id
    await subscription_crud.create_subscription(
        db=db,
        user_db_id=user_db_id,
        name=sub_name,
        url=sub_url
    )

async def delete_subscription_service(db, telegram_id : int, sub_name : str):
    user_db_id = await user_crud.get_db_user_id(db, telegram_id)
    return await subscription_crud.delete_sub(db, user_db_id, sub_name)

async def get_users_subs_service(db, telegram_id : int):
    user_db_id = await user_crud.get_db_user_id(db, telegram_id)
    return await subscription_crud.get_user_subs_by_id(db, user_db_id)