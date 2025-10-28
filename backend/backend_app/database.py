# backend/backend_app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.backend_app.core.config import settings

Base = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    future=True
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# dependency FastAPI
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# Hàm tạo bảng
async def init_db():
    from backend.backend_app.core.seed_admin import seed_admin

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Tạo admin mặc định
    async with AsyncSessionLocal() as session:
        await seed_admin(session)


