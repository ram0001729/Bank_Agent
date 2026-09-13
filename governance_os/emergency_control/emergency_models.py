from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class RevocationScope(str, Enum):

    AGENT = "agent"
    FLEET = "fleet"


class RevocationStatus(str, Enum):

    ACTIVE = "active"
    REVOKED = "revoked"


class RevocationRecord(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    revocation_id: str

    scope: RevocationScope

    agent_id: str | None = None

    status: RevocationStatus

    reason: str

    revoked_by: str

    revoked_at: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    expires_at: datetime | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )


class EmergencyStopResult(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    success: bool

    scope: RevocationScope

    agent_id: str | None = None

    message: str

    revocation_id: str

    revoked_at: datetime