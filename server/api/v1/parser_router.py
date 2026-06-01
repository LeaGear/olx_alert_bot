import logging

from fastapi import APIRouter, HTTPException, status, Depends

from typing import List

from server.db.database import get_db
from server.core.parser_service import get_all_users_subs_service

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
)


# WAY - /v1/parser/update_users_subs
@router.post("/update_users_subs", status_code=status.HTTP_200_OK)
async def update_users_subs(db=Depends(get_db)):
    pass


# WAY - /v1/parser/get_all_users_subs
@router.get("/get_all_users_subs", status_code=status.HTTP_200_OK)
async def get_all_users_subs(db=Depends(get_db)):
    result = await get_all_users_subs_service(db)
    logging.error(f"result = {result}")
    return result
