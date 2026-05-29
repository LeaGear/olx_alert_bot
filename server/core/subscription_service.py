import logging

from server.crud import user_crud, subscription_crud




async def add_subscription_service(db, user_id : int, sub_name : str, sub_url : str):
    logging.error("SERVICE WORK IS STARTING!!!!!!!!!!----------------------------------->>>>>>")
    user = await user_crud.get_user_by_id(db, user_id)
    logging.error("USER NOT FOUND IN TABLE USERS------------------------------------------<<<<<<<<<<<<<<<<<<<")
    if not user:
        await user_crud.create_user(db, user_id)

    await subscription_crud.create_subscription(
        db=db,
        user_id=user_id,
        name=sub_name,
        url=sub_url
    )