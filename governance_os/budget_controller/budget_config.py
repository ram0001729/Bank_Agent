from decimal import Decimal

from governance.budget_controller.limits import (
    AgentBudgetLimit,
    get_agent_budget,
)


class BudgetConfig:

    CURRENCY = "INR"

    WARNING_THRESHOLD = Decimal(
        "0.80"
    )

    ESCALATION_THRESHOLD = Decimal(
        "0.90"
    )

    @classmethod
    def get_agent_limit(
        cls,
        agent_type: str,
    ) -> AgentBudgetLimit:

        return get_agent_budget(
            agent_type
        )