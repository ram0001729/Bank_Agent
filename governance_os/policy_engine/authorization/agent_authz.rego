package agent.authz

import future.keywords.in

default allow = false

# Role permissions mapping
role_permissions := {
    "supervisor": ["TRANSFER", "LOAN_APPROVAL", "REFUND", "POLICY_QUERY", "RISK_CHECK"],
    "fraud_evaluator": ["RISK_CHECK", "POLICY_QUERY"],
    "loan_underwriter": ["LOAN_APPROVAL", "POLICY_QUERY"],
    "refund_processor": ["REFUND", "POLICY_QUERY"],
    "support_assistant": ["POLICY_QUERY"]
}

# Policy Limits
max_transfer_amount := 5000.0
max_refund_amount := 500.0
max_loan_amount := 50000.0
max_risk_threshold := 0.70

# Allow rule: Must satisfy all conditions
allow {
    not input.emergency_stop_active
    input.action in role_permissions[input.role]
    input.risk_score <= max_risk_threshold
    amount_within_limits
}

amount_within_limits {
    input.action == "TRANSFER"
    input.amount <= max_transfer_amount
}

amount_within_limits {
    input.action == "REFUND"
    input.amount <= max_refund_amount
}

amount_within_limits {
    input.action == "LOAN_APPROVAL"
    input.amount <= max_loan_amount
}

amount_within_limits {
    input.action == "POLICY_QUERY"
}

amount_within_limits {
    input.action == "RISK_CHECK"
}
