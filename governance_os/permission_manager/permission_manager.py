from typing import List


class PermissionManager:
    """RBAC / ABAC Access Control Manager."""
    def __init__(self):
        self.role_permissions = {
            "supervisor": ["TRANSFER", "LOAN_APPROVAL", "REFUND", "POLICY_QUERY", "RISK_CHECK"],
            "fraud_evaluator": ["RISK_CHECK", "POLICY_QUERY"],
            "loan_underwriter": ["LOAN_APPROVAL", "POLICY_QUERY"],
            "refund_processor": ["REFUND", "POLICY_QUERY"],
            "support_assistant": ["POLICY_QUERY"]
        }

    def check_permission(self, role: str, action: str) -> bool:
        allowed = self.role_permissions.get(role, [])
        return action in allowed
