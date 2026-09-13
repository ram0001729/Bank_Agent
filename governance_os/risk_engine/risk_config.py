from dataclasses import dataclass


@dataclass(frozen=True)
class RiskThresholds:

    low_max: float = 0.20

    medium_max: float = 0.50

    high_max: float = 0.80

    critical_max: float = 1.00


@dataclass(frozen=True)
class RiskDecisionThresholds:

    review_threshold: float = 0.50

    block_threshold: float = 0.80