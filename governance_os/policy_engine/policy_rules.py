from dataclasses import dataclass


@dataclass(frozen=True)
class RefundPolicy:

    customer_limit: float = 25_000

    employee_limit: float = 100_000

    high_value_threshold: float = 25_000

    approval_threshold: float = 10_000


@dataclass(frozen=True)
class LoanPolicy:

    maximum_loan_amount: float = 1_000_000

    minimum_credit_score: int = 650

    manual_review_score: int = 700


@dataclass(frozen=True)
class TransactionPolicy:

    maximum_transaction_amount: float = 500_000

    high_value_threshold: float = 100_000