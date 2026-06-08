import logging

from fastapi import APIRouter, HTTPException, status, Depends


from my_shared import APIResponse
from server.db.database import get_db
from server.core.parser_service import get_all_users_subs_service, update_users_data_service

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
)


# WAY - /{API_VERSION}/parser/update_users_subs
@router.post("/update_users_subs", status_code=status.HTTP_200_OK)
async def update_users_subs(new_data: APIResponse, db=Depends(get_db)):
    logging.error(f"I GOT NEW DATA !!!!!!!!!!!!!!!!!!!!!!!!!!!!!! - - - -  {new_data}")
    if new_data.ok:
        await update_users_data_service(new_data.data, db)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


# WAY - /{API_VERSION}/parser/get_all_users_subs
@router.get("/get_all_users_subs", status_code=status.HTTP_200_OK)
async def get_all_users_subs(db=Depends(get_db)):
    result = await get_all_users_subs_service(db)
    return result
