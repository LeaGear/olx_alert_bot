import logging

from fastapi import APIRouter, HTTPException, status, Depends

from typing import List

from server.db.database import get_db
from server.crud import subscription_crud, user_crud
from server.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from server.core.subscription_service import add_subscription_service

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)

#WAY - /subscriptions/add
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_subscription(sub_data: SubscriptionCreate, db=Depends(get_db)) -> dict:
    logging.error(f"SERVER GET DATA FOR ADDING ___+_++_+++_+_+_+_+_+_+_+     {sub_data}")
    await add_subscription_service(db, sub_data.telegram_id, sub_data.name, sub_data.url)

    print(f"New subscription created for {sub_data.telegram_id} with {sub_data.name} and url - {sub_data.url}")

    return {
        "status": "success",
        "detail": "add_success",
    }

#WAY = /subscriptions/{telegram_id}
@router.get("/{telegram_id}", response_model=List[SubscriptionResponse])
async def get_user_subscriptions(telegram_id: int, db=Depends(get_db)) -> List[dict]:
    user_db_id = await user_crud.get_db_user_id(db, telegram_id)
    subs = await subscription_crud.get_user_subs_by_id(db, user_db_id)
    return subs


#WAY /subscriptions/{telegram_id}/delete/{sub_name}
@router.delete("/{telegram_id}/delete/{sub_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_subscription(telegram_id: int, sub_name: str, db=Depends(get_db)):
    db_response = await subscription_crud.delete_sub(db, telegram_id, sub_name)
    logging.error(db_response)
    if not db_response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)