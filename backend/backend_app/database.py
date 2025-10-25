# backend/backend_app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker,declarative_base

DATABASE_URL = "mysql+aiomysql://root:namnguyenngoc2608%40@localhost:3306/new_daca"

engine = create_async_engine(
    DATABASE_URL,
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
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

Base = declarative_base()
