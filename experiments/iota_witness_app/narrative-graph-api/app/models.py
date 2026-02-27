from __future__ import annotations

from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app import __version__


class NodeType(StrEnum):
    IDENTITY = "identity"
    ENACTMENT = "enactment"
    EFFECT = "effect"
    SETTING = "setting"
    CHARACTER = "character"
    DIALOGUE = "dialogue"
    THEME = "theme"


class EdgeType(StrEnum):
    GROUNDS = "grounds"
    PRODUCES = "produces"
    IMPLIES = "implies"
    COHERES = "coheres"
    FULFILLS = "fulfills"
    CONTRASTS = "contrasts"
    PARALLELS = "parallels"


class LogosReference(BaseModel):
    resource_id: str = Field(..., description="Logos resource ID")
    passage: str = Field(..., description="Bible reference")
    include_original_language: bool = False
    include_morphology: bool = False
    include_crossrefs: bool = True

    @field_validator("passage")
    @classmethod
    def validate_passage(cls, value: str) -> str:
        if len(value.strip()) < 3:
            raise ValueError("Invalid passage reference")
        return value


class NarrativeNode(BaseModel):
    id: str
    type: NodeType
    text: str
    reference: str
    lemmas: list[str] = Field(default_factory=list)
    strongs_numbers: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0, default=0.75)
    metadata: dict[str, Any] = Field(default_factory=dict)


class NarrativeEdge(BaseModel):
    id: str
    from_id: str
    to_id: str
    type: EdgeType
    confidence: float = Field(ge=0.0, le=1.0)
    theological_weight: float = Field(ge=0.0, le=1.0, default=0.5)
    cross_references: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Motif(BaseModel):
    name: str
    confidence: float = Field(ge=0.0, le=1.0)
    occurrences: list[str] = Field(default_factory=list)
    cross_references: list[str] = Field(default_factory=list)
    description: str


class ParallelGospel(BaseModel):
    gospel: str
    reference: str
    graph_differences: dict[str, Any] = Field(default_factory=dict)
    theological_significance: str | None = None


class NarrativeGraph(BaseModel):
    id: str
    primary_reference: str
    nodes: list[NarrativeNode]
    edges: list[NarrativeEdge]
    motifs: list[Motif] = Field(default_factory=list)
    parallels: dict[str, ParallelGospel] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class NarrativeResponse(BaseModel):
    success: bool
    graph: NarrativeGraph | None = None
    cached: bool = False
    processing_time_ms: int = 0
    error: str | None = None
    api_version: str = __version__


class LogosIntegrationResponse(BaseModel):
    html_panel: str
    json_data: dict[str, Any]
    export_formats: dict[str, str]


class NarrativeAnalyzeRequest(BaseModel):
    passage: str
    text: str | None = None
    resource_id: str = "LSS:ESV"
    include_original_language: bool = False
    include_morphology: bool = False
    include_crossrefs: bool = True
    include_parallels: bool = True
    include_logos_format: bool = True


class NarrativeAnalyzeResult(BaseModel):
    response: NarrativeResponse
    logos: LogosIntegrationResponse | None = None
