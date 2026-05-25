from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel, Field, field_validator
import re
from typing import Optional, List

from server.database import engine, Base, get_db
from server import crud


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="OLX Alert API", lifespan=lifespan)


class SubscriptionCreate(BaseModel):
    user_id: int = Field(description = "Telegram ID пользователя")
    name: str = Field(description = "Название подписки")
    url: str = Field(description = "Ссылка на OLX с фильтрами или без")
    content: List[dict] = []
    content_hash: Optional[str] = None


    @field_validator("url")
    @classmethod
    def validate_olx_url(cls, v: str) -> str:
        olx_pattern = r"^https?://(?:www\.)?olx\.ua/.*"

        if not re.match(olx_pattern, v):
            raise ValueError("Ссылка должна быть валидным URL-адресом платформы OLX.ua")

        return v


@app.get("/")
async def root():
    return {"message": "Server is up. Go working!"}


@app.post("/add_subscription", status_code=status.HTTP_201_CREATED)
async def add_subscription(sub_data: SubscriptionCreate, db=Depends(get_db)):

    user = await crud.get_user_by_id(db, sub_data.user_id)
    if not user:
        user = await crud.create_user(db, sub_data.user_id)

    new_sub = await crud.create_subscription(
        db=db,
        user_id=user.id,
        name=sub_data.name,
        url=sub_data.url
    )
    print(f"New subscription created for {sub_data.user_id} with {sub_data.name} and url - {sub_data.url}")

    return {
        "status": "success",
        "message": "New subscription created successfully",
        "subscription_id": new_sub.id
    }
