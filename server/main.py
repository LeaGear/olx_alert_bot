from fastapi import FastAPI
from contextlib import asynccontextmanager

from server.db.database import engine
from server.db.base import Base
from server.api.base_router import main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(title="OLX Alert API", lifespan=lifespan)

app.include_router(main_router)


@app.get("/")
async def root():
    return {"message": "Server is up. Go working!"}
