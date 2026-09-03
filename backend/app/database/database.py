from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.config import get_settings
from app.database.models import Base
from app.utils.logger import logger

settings = get_settings()

engine = create_async_engine(
    f"sqlite+aiosqlite:///{settings.memory_db_path}",
    echo=settings.debug,
)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info(f"Database initialized at {settings.memory_db_path}")


async def get_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
