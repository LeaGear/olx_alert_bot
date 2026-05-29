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
