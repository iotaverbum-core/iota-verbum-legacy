from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class EntryRequest(BaseModel):
    device_id: str = Field(min_length=3, max_length=128)
    text: str = Field(min_length=1, max_length=4000)
    ai_consent: bool = False
    local_only: bool = False


class EntryResponse(BaseModel):
    eden_text: str
    modal: dict[str, Any]
    attestation: dict[str, Any]
    local_mode: bool = False
    crisis_flag: bool = False
    entry_id: str


class MomentResponse(BaseModel):
    eden_text: str
    modal: dict[str, Any]
    attestation: dict[str, Any]
    local_mode: bool = False
    crisis_flag: bool = False
    moment_id: str


class TraceResponse(BaseModel):
    device_id: str
    dominant_distortion: str
    velocity_trend: float
    hinge_consistency: float
    entrustment_stability: float
    sample_count: int
    updated_at: datetime
