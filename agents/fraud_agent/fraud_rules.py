from dataclasses import dataclass


@dataclass(frozen=True)
class FraudRuleResult:

    rule_triggered: bool
    rule_name: str | None
    reason: str | None


class FraudRules:

    def evaluate(
        self,
        transaction: dict
    ) -> FraudRuleResult:

        amount = float(
            transaction.get(
                "amount",
                0
            )
        )

        new_device = bool(
            transaction.get(
                "new_device",
                False
            )
        )

        unusual_location = bool(
            transaction.get(
                "unusual_location",
                False
            )
        )

        if (
            amount >= 100000
            and new_device
        ):

            return FraudRuleResult(
                rule_triggered=True,
                rule_name="HIGH_VALUE_NEW_DEVICE",
                reason=(
                    "High-value transaction "
                    "from a new device."
                ),
            )

        if (
            amount >= 50000
            and unusual_location
        ):

            return FraudRuleResult(
                rule_triggered=True,
                rule_name="HIGH_VALUE_UNUSUAL_LOCATION",
                reason=(
                    "High-value transaction "
                    "from an unusual location."
                ),
            )

        return FraudRuleResult(
            rule_triggered=False,
            rule_name=None,
            reason=None,
        )