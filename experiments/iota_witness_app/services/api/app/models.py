from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel


class SeasonEntry(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    device_id: str = Field(index=True)
    text_hash: str
    modal: dict[str, Any] = Field(sa_column=Column(JSON))
    hinge_action: str = ""
    eden_text: str | None = None
    attestation: dict[str, Any] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None),
        index=True,
    )


class MomentEntry(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    device_id: str = Field(index=True)
    text_hash: str
    modal: dict[str, Any] = Field(sa_column=Column(JSON))
    hinge_action: str = ""
    eden_text: str | None = None
    attestation: dict[str, Any] = Field(sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC).replace(tzinfo=None),
        index=True,
    )
