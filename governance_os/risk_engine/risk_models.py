from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RiskLevel(str, Enum):

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskDecision(str, Enum):

    ALLOW = "allow"
    REVIEW = "review"
    BLOCK = "block"


class RiskRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    agent_id: str
    agent_name: str
    agent_type: str

    action: str
    resource: str

    user_id: str | None = None

    amount: float | None = Field(
        default=None,
        ge=0
    )

    features: dict[str, Any] = Field(
        default_factory=dict
    )

    context: dict[str, Any] = Field(
        default_factory=dict
    )


class RiskAssessment(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    model_name: str

    model_version: str | None = None

    fraud_probability: float = Field(
        ge=0.0,
        le=1.0
    )

    risk_score: float = Field(
        ge=0.0,
        le=100.0
    )

    risk_level: RiskLevel

    decision: RiskDecision

    reason: str

    triggered_rules: list[str] = Field(
        default_factory=list
    )

    model_metadata: dict[str, Any] = Field(
        default_factory=dict
    )