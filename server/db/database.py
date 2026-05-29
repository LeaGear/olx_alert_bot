from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from server.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=True)

async_session = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit=False
)



async def get_db():
    async with async_session() as session:
        yield session