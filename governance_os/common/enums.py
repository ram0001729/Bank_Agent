from enum import Enum


class ActionType(str, Enum):
    TRANSFER = "TRANSFER"
    LOAN_APPROVAL = "LOAN_APPROVAL"
    REFUND = "REFUND"
    POLICY_QUERY = "POLICY_QUERY"
    RISK_CHECK = "RISK_CHECK"


class GovernanceDecision(str, Enum):
    ALLOW = "ALLOW"
    DENY = "DENY"
    FLAGGED = "FLAGGED"
    REQUIRES_MFA = "REQUIRES_MFA"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"
