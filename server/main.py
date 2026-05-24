from fastapi import FastAPI, HTTPException, status, Depends
from contextlib import asynccontextmanager
from pydantic import BaseModel, HttpUrl
from typing import Optional, List


from server.database import engine, Base, get_db
# Обязательно импортируем модели, чтобы SQLAlchemy знала об их существовании при создании таблиц
from server.models.subscription import User, Subscription



@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield



app = FastAPI(title="OLX Alert API")


class SubscriptionCreate(BaseModel):
    user_id: int
    name: str
    url: str
    content: List[dict] = []
    content_hash: Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Server is up. Go working!"}


@app.post("/add_subscription", status_code=status.HTTP_201_CREATED)
async def add_subscription(sub_data: SubscriptionCreate, db = Depends(get_db)):
    if "olx.ua" not in sub_data.url:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL. URL must contains 'olx.ua'")

    print(f"New subscription created for {sub_data.user_id} with {sub_data.name} and url - {sub_data.url}")

    return{
        "status" : "success",
        "message" : "New subscription created successfully",
        "payload" : sub_data
    }