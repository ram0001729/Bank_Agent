from typing import Tuple
from governance_os.permission_manager.opa_client import OPAClient


class PolicyEngine:
    """OPA Rego Policy Engine for financial governance allow/deny decisions."""
    def __init__(self):
        self.opa_client = OPAClient()

    def evaluate_policy(
        self,
        action: str,
        amount: float,
        risk_score: float,
        role: str = "supervisor"
    ) -> Tuple[bool, str]:
        return self.opa_client.evaluate_rego_policy(
            role=role,
            action=action,
            amount=amount,
            risk_score=risk_score
        )
