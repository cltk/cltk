"""Pydantic models describing declarative pipelines."""

from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class StepSpec(BaseModel):
    """Single pipeline step definition."""

    id: str
    enabled: bool = True
    config: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "forbid"}


class PipelineSpec(BaseModel):
    """Declarative pipeline definition."""

    preset: Optional[str] = None
    language: Optional[str] = None
    steps: Optional[list[StepSpec]] = None
    step_overrides: dict[str, dict[str, Any]] = Field(default_factory=dict)
    meta: dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "forbid"}
