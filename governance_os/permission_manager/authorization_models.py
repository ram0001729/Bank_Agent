from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AuthorizationRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    agent_id: str
    agent_name: str
    agent_type: str
    agent_version: str

    action: str
    resource: str

    user_id: str | None = None

    environment: str = "development"

    context: dict[str, Any] = Field(
        default_factory=dict
    )


class AuthorizationDecision(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    allowed: bool

    reason: str

    policy: str | None = None

    matched_rules: list[str] = Field(
        default_factory=list
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )