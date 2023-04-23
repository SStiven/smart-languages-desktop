from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

user = "cache_admin"
password = "cache_password"
host = "localhost"
port = "5432"
database_name = "cache"

async_engine = create_async_engine(
    f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}"
)

session_factory = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)
