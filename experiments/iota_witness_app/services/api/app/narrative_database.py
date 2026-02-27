from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, Integer, JSON, String
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AnalysisJob(Base):
    __tablename__ = "narrative_analysis_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reference: Mapped[str] = mapped_column(String, nullable=False)
    resource_id: Mapped[str] = mapped_column(String, nullable=False)
    processing_time_ms: Mapped[int] = mapped_column(Integer, default=0)
    nodes_count: Mapped[int] = mapped_column(Integer, default=0)
    edges_count: Mapped[int] = mapped_column(Integer, default=0)
    motifs_found: Mapped[list[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    api_version: Mapped[str] = mapped_column(String, default="1.0.0")


class PopularPassage(Base):
    __tablename__ = "narrative_popular_passages"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reference: Mapped[str] = mapped_column(String, unique=True, index=True)
    analysis_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_processing_time: Mapped[float] = mapped_column(Float, default=0.0)
    last_analyzed: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    cached_version: Mapped[str | None] = mapped_column(String, nullable=True)


class NarrativeDatabase:
    def __init__(self, database_url: str) -> None:
        self.engine = create_async_engine(database_url, echo=False)
        self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    async def create_tables(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def record_analysis(self, payload: dict[str, Any]) -> None:
        async with self.session_factory() as session:
            session.add(AnalysisJob(**payload))
            await session.commit()
