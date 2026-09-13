from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AuditEventType(str, Enum):

    AGENT_REGISTERED = "agent_registered"
    AGENT_UNREGISTERED = "agent_unregistered"

    PERMISSION_CHECK = "permission_check"

    POLICY_EVALUATION = "policy_evaluation"

    RISK_ASSESSMENT = "risk_assessment"

    BUDGET_EVALUATION = "budget_evaluation"

    GOVERNANCE_DECISION = "governance_decision"

    MCP_REQUEST = "mcp_request"

    MCP_EXECUTION = "mcp_execution"

    MCP_FAILURE = "mcp_failure"

    EMERGENCY_STOP = "emergency_stop"


class AuditSeverity(str, Enum):

    INFO = "info"
    WARNING = "warning"
    HIGH = "high"
    CRITICAL = "critical"


class AuditEvent(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    event_id: str

    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(
            timezone.utc
        )
    )

    event_type: AuditEventType

    severity: AuditSeverity = (
        AuditSeverity.INFO
    )

    request_id: str

    agent_id: str | None = None

    agent_name: str | None = None

    agent_type: str | None = None

    user_id: str | None = None

    action: str | None = None

    resource: str | None = None

    amount: Decimal | None = None

    currency: str | None = None

    decision: str | None = None

    reason: str | None = None

    policy_name: str | None = None

    policy_version: str | None = None

    risk_level: str | None = None

    fraud_probability: float | None = None

    risk_score: float | None = None

    budget_limit: Decimal | None = None

    remaining_budget: Decimal | None = None

    mcp_server: str | None = None

    mcp_tool: str | None = None

    success: bool | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )