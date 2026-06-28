import asyncio
import os
from typing import AsyncGenerator

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://optimizer:optimizer@localhost:5432/optimizer",
)

_engine: AsyncEngine | None = None
_engine_loop: asyncio.AbstractEventLoop | None = None


def get_engine() -> AsyncEngine:
    global _engine, _engine_loop
    try:
        current_loop = asyncio.get_running_loop()
    except RuntimeError:
        current_loop = None

    if _engine is None or _engine_loop is not current_loop:
        _engine = create_async_engine(DATABASE_URL, echo=False)
        _engine_loop = current_loop
    return _engine


def set_engine(url: str) -> AsyncEngine:
    global _engine, _engine_loop
    _engine = create_async_engine(url, echo=False)
    try:
        _engine_loop = asyncio.get_running_loop()
    except RuntimeError:
        _engine_loop = None
    return _engine


def get_session_maker() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(get_engine(), class_=AsyncSession, expire_on_commit=False)


async def dispose_engine() -> None:
    global _engine, _engine_loop
    if _engine is not None:
        try:
            await _engine.dispose()
        except Exception:
            pass
        _engine = None
    _engine_loop = None


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
    async with get_engine().begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await dispose_engine()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with get_session_maker()() as session:
        yield session
