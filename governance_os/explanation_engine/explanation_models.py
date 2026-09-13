from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ExplanationResult(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    decision: str

    summary: str

    detailed_explanation: str

    reasons: list[str] = Field(
        default_factory=list
    )

    required_action: str | None = None

    evidence: list[str] = Field(
        default_factory=list
    )

    confidence: float = 1.0

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )