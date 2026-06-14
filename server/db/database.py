from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from server.config import DATABASE_URL

#Connecting to database server(Postgres SQL)
engine = create_async_engine(DATABASE_URL, echo=True) #echo for print sql-requests in console

async_session = async_sessionmaker(
    bind = engine,
    class_ = AsyncSession,
    expire_on_commit=False
)


#Function for working with server requests
async def get_db():
    async with async_session() as session:
        yield session