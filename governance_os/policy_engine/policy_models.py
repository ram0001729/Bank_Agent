from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class PolicyDecision(str, Enum):

    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


class PolicyRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    agent_id: str
    agent_name: str
    agent_type: str

    user_id: str | None = None

    action: str
    resource: str

    amount: float | None = Field(
        default=None,
        ge=0
    )

    risk_level: str | None = None

    environment: str = "development"

    context: dict[str, Any] = Field(
        default_factory=dict
    )


class PolicyResult(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    decision: PolicyDecision

    policy_name: str

    reason: str

    matched_rules: list[str] = Field(
        default_factory=list
    )

    required_approval: bool = False

    approval_role: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )

    policy_context: str | None = None

    policy_sources: list[dict] = Field(
        default_factory=list
    )