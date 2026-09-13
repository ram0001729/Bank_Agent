import os
import requests
from typing import Dict, Any, Tuple


class OPAClient:
    """Open Policy Agent (OPA) Rego Policy Client & Evaluator."""
    def __init__(self, opa_url: str = None):
        self.opa_url = opa_url or os.getenv("OPA_URL", "http://localhost:8181/v1/data/agent/authz/allow")

    def evaluate_rego_policy(
        self,
        role: str,
        action: str,
        amount: float,
        risk_score: float,
        emergency_stop_active: bool = False
    ) -> Tuple[bool, str]:
        input_payload = {
            "input": {
                "role": role,
                "action": action,
                "amount": amount,
                "risk_score": risk_score,
                "emergency_stop_active": emergency_stop_active
            }
        }

        # 1. Attempt connection to live OPA REST API if running
        try:
            res = requests.post(self.opa_url, json=input_payload, timeout=0.5)
            if res.status_code == 200:
                result = res.json().get("result", False)
                reason = "OPA Rego Policy: ALLOWED" if result else "OPA Rego Policy: DENIED by Rego policy rules"
                return result, reason
        except Exception:
            pass  # Fall back to local Rego engine evaluation

        # 2. Local Rego Engine Evaluation matching agent_authz.rego
        if emergency_stop_active:
            return False, "OPA Rego Evaluation: DENIED (emergency_stop_active is True)"

        role_permissions = {
            "supervisor": ["TRANSFER", "LOAN_APPROVAL", "REFUND", "POLICY_QUERY", "RISK_CHECK"],
            "fraud_evaluator": ["RISK_CHECK", "POLICY_QUERY"],
            "loan_underwriter": ["LOAN_APPROVAL", "POLICY_QUERY"],
            "refund_processor": ["REFUND", "POLICY_QUERY"],
            "support_assistant": ["POLICY_QUERY"]
        }

        allowed_actions = role_permissions.get(role, [])
        if action not in allowed_actions:
            return False, f"OPA Rego Evaluation: DENIED (Role '{role}' unpermitted for action '{action}')"

        if risk_score > 0.70:
            return False, f"OPA Rego Evaluation: DENIED (Risk score {risk_score:.2f} > max 0.70)"

        if action == "TRANSFER" and amount > 5000.0:
            return False, f"OPA Rego Evaluation: DENIED (Transfer amount ${amount:.2f} > max $5000.00)"

        if action == "REFUND" and amount > 500.0:
            return False, f"OPA Rego Evaluation: DENIED (Refund amount ${amount:.2f} > max $500.00)"

        if action == "LOAN_APPROVAL" and amount > 50000.0:
            return False, f"OPA Rego Evaluation: DENIED (Loan amount ${amount:.2f} > max $50000.00)"

        return True, "OPA Rego Evaluation: ALLOWED"
