from response_kit import log_function, logger, APIResponse

from server.crud import subscription_crud
from server.core import comparison_service, notification_service, id_replace_service

@log_function
async def get_all_users_subs_service(db):
    result = await subscription_crud.get_all_subs(db)
    return result

async def update_users_data_service(new_data, db):
    logger.info("Starting function - <<update_users_data_service>>")
    try:
        new_content = await comparison_service.get_only_new(new_data)
        logger.info("Data obtained after comparison")

        new_content = await id_replace_service.replacer(db, new_content)
        logger.info("Id replaced successfully")

        await notification_service.notificator(new_content)
        logger.info("Users were successfully notified")

        await subscription_crud.update_subscriptions(db, new_data)
        logger.info("DATABASE were updated successfully")

        logger.info("Finished function - <<update_users_data_service>>")
        return APIResponse(status="success")

    except Exception as e:
        logger.error(f"Comparison failed - ERROR - >{e}<", exc_info=True)
        return APIResponse(status="error")
