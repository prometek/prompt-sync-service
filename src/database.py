from sqlmodel import SQLModel, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import select
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./data/prompts.db")

def create_db_and_tables():
    engine = create_async_engine(DATABASE_URL, echo=True)
    SQLModel.metadata.create_all(engine)

# Async engine and session
async_engine = create_async_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})
async def get_session() -> AsyncSession:
    async with AsyncSession(async_engine) as session:
        yield session
