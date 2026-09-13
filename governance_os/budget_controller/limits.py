from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class AgentBudgetLimit:

    per_request_limit: Decimal

    daily_limit: Decimal

    monthly_limit: Decimal


LOAN_AGENT_BUDGET = AgentBudgetLimit(
    per_request_limit=Decimal("500000"),
    daily_limit=Decimal("10000000"),
    monthly_limit=Decimal("100000000"),
)


REFUND_AGENT_BUDGET = AgentBudgetLimit(
    per_request_limit=Decimal("25000"),
    daily_limit=Decimal("250000"),
    monthly_limit=Decimal("2500000"),
)


FRAUD_AGENT_BUDGET = AgentBudgetLimit(
    per_request_limit=Decimal("100000"),
    daily_limit=Decimal("500000"),
    monthly_limit=Decimal("5000000"),
)


SUPPORT_AGENT_BUDGET = AgentBudgetLimit(
    per_request_limit=Decimal("5000"),
    daily_limit=Decimal("25000"),
    monthly_limit=Decimal("250000"),
)


SUPERVISOR_AGENT_BUDGET = AgentBudgetLimit(
    per_request_limit=Decimal("100000"),
    daily_limit=Decimal("1000000"),
    monthly_limit=Decimal("10000000"),
)


DEFAULT_AGENT_BUDGET = AgentBudgetLimit(
    per_request_limit=Decimal("1000"),
    daily_limit=Decimal("5000"),
    monthly_limit=Decimal("50000"),
)


AGENT_BUDGETS = {

    "loan": LOAN_AGENT_BUDGET,

    "refund": REFUND_AGENT_BUDGET,

    "fraud": FRAUD_AGENT_BUDGET,

    "support": SUPPORT_AGENT_BUDGET,

    "supervisor": SUPERVISOR_AGENT_BUDGET,
}


def get_agent_budget(
    agent_type: str,
) -> AgentBudgetLimit:

    return AGENT_BUDGETS.get(
        agent_type,
        DEFAULT_AGENT_BUDGET
    )