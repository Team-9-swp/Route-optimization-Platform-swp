import os
from typing import AsyncGenerator

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base

Base = declarative_base()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://optimizer:optimizer@localhost:5432/optimizer",
)

engine = create_async_engine(DATABASE_URL, echo=False)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class JobModel(Base):
    __tablename__ = "jobs"

    job_id = Column(String(36), primary_key=True)
    status = Column(String(20), nullable=False, default="pending")
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    seed = Column(Integer, nullable=False, default=42)
    time_limit = Column(Float, nullable=True)
    input_data = Column(JSON, nullable=False, default=dict)
    result = Column(JSON, nullable=True)
    error = Column(Text, nullable=True)
    objective_value = Column(Float, nullable=True)
    validation_status = Column(String(20), nullable=True)
    validation_report = Column(JSON, nullable=True)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
