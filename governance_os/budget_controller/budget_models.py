from decimal import Decimal
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BudgetDecision(str, Enum):

    ALLOW = "allow"
    DENY = "deny"
    ESCALATE = "escalate"


class BudgetRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    agent_id: str
    agent_name: str
    agent_type: str

    action: str
    resource: str

    authorized_amount: Decimal = Field(
        ge=Decimal("0")
    )

    currency: str = "INR"

    user_id: str | None = None

    context: dict[str, Any] = Field(
        default_factory=dict
    )


class BudgetAssessment(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    agent_id: str
    agent_name: str
    agent_type: str

    decision: BudgetDecision

    authorized_amount: Decimal

    per_request_limit: Decimal

    daily_budget_limit: Decimal

    monthly_budget_limit: Decimal

    current_daily_authorized: Decimal

    current_monthly_authorized: Decimal

    remaining_daily_budget: Decimal

    remaining_monthly_budget: Decimal

    daily_utilization_percent: Decimal

    monthly_utilization_percent: Decimal

    reason: str

    triggered_rules: list[str] = Field(
        default_factory=list
    )

    currency: str = "INR"