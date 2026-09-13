from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ActionStatus(str, Enum):

    APPROVED = "approved"
    CONSUMED = "consumed"
    REVOKED = "revoked"
    EXPIRED = "expired"


class ApprovedAction(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    action_id: str

    request_id: str

    agent_id: str

    agent_name: str

    agent_type: str

    user_id: str | None = None

    action: str

    resource: str

    mcp_server: str

    mcp_tool: str

    status: ActionStatus = (
        ActionStatus.APPROVED
    )

    amount: float | None = None

    currency: str = "INR"

    issued_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    expires_at: datetime

    consumed_at: datetime | None = None

    governance_decision: str = "allow"

    governance_snapshot: dict[str, Any] = (
        Field(
            default_factory=dict
        )
    )

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )