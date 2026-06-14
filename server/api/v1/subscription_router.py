from fastapi import APIRouter, HTTPException, status, Depends

from typing import List

from server.db.database import get_db
from server.schemas.subscription import SubscriptionCreate, SubscriptionResponse
from server.core.subscription_service import add_subscription_service, delete_subscription_service, get_users_subs_service

router = APIRouter(
    prefix="/subscriptions",
    tags=["subscriptions"]
)

#WAY - /{API_VERSION}/subscriptions/add
@router.post("/add", status_code=status.HTTP_201_CREATED)
async def add_subscription(sub_data: SubscriptionCreate, db=Depends(get_db)):

    await add_subscription_service(db, sub_data.telegram_id, sub_data.name, sub_data.url)


#WAY = /{API_VERSION}/subscriptions/{telegram_id}
@router.get("/{telegram_id}", response_model=List[SubscriptionResponse])
async def get_user_subscriptions(telegram_id: int, db=Depends(get_db)) -> List[SubscriptionResponse]:
    subs = await get_users_subs_service(db, telegram_id)
    if subs:
        return subs
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user_not_found")


#WAY /{API_VERSION}/subscriptions/{telegram_id}/delete/{sub_name}
@router.delete("/{telegram_id}/delete/{sub_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_subscription(telegram_id: int, sub_name: str, db=Depends(get_db)):
    response = await delete_subscription_service(db, telegram_id, sub_name)
    if not response:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)