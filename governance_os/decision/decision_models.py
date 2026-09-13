from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class GovernanceDecision(str, Enum):

    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


class ComponentDecision(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    decision: str

    reason: str = ""

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class GovernanceEvaluation(BaseModel):

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

    amount: float | None = None

    currency: str = "INR"

    opa: ComponentDecision

    policy: ComponentDecision

    risk: ComponentDecision

    budget: ComponentDecision


class GovernanceDecisionResult(BaseModel):

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

    amount: float | None = None

    currency: str = "INR"

    decision: GovernanceDecision

    reason: str

    blocking_components: list[str] = Field(
        default_factory=list
    )

    escalation_components: list[str] = Field(
        default_factory=list
    )

    opa: ComponentDecision

    policy: ComponentDecision

    risk: ComponentDecision

    budget: ComponentDecision

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )