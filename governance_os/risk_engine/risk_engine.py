import sys

from governance.risk.risk_config import (
    RiskDecisionThresholds,
    RiskThresholds,
)

from governance.risk.risk_models import (
    RiskAssessment,
    RiskDecision,
    RiskLevel,
    RiskRequest,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class RiskEngine:

    def __init__(
        self,
        model,
        model_name: str = "fraud_detection_model",
        model_version: str | None = None,
        risk_thresholds: RiskThresholds | None = None,
        decision_thresholds: (
            RiskDecisionThresholds | None
        ) = None,
    ):

        self.model = model

        self.model_name = model_name

        self.model_version = model_version

        self.risk_thresholds = (
            risk_thresholds
            if risk_thresholds is not None
            else RiskThresholds()
        )

        self.decision_thresholds = (
            decision_thresholds
            if decision_thresholds is not None
            else RiskDecisionThresholds()
        )

        logger.info(
            "Risk engine initialized"
        )

    def assess(
        self,
        request: RiskRequest,
    ) -> RiskAssessment:

        try:

            logger.info(
                f"Starting risk assessment: "
                f"request_id={request.request_id}, "
                f"agent={request.agent_name}, "
                f"action={request.action}"
            )

            probability = (
                self._predict_fraud_probability(
                    request
                )
            )

            risk_level = (
                self._get_risk_level(
                    probability
                )
            )

            decision = (
                self._get_decision(
                    probability
                )
            )

            triggered_rules = (
                self._get_triggered_rules(
                    probability,
                    risk_level,
                    decision,
                )
            )

            reason = (
                self._build_reason(
                    probability,
                    risk_level,
                    decision,
                    triggered_rules,
                )
            )

            risk_score = (
                probability * 100
            )

            assessment = RiskAssessment(
                request_id=request.request_id,

                model_name=self.model_name,

                model_version=(
                    self.model_version
                ),

                fraud_probability=(
                    probability
                ),

                risk_score=risk_score,

                risk_level=risk_level,

                decision=decision,

                reason=reason,

                triggered_rules=(
                    triggered_rules
                ),

                model_metadata={
                    "agent_id": request.agent_id,
                    "agent_name": request.agent_name,
                    "agent_type": request.agent_type,
                    "action": request.action,
                    "resource": request.resource,
                },
            )

            logger.info(
                f"Risk assessment completed: "
                f"probability={probability:.4f}, "
                f"risk_level={risk_level.value}, "
                f"decision={decision.value}"
            )

            return assessment

        except Exception as e:

            logger.exception(
                "Risk assessment failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # MODEL PREDICTION
    # ========================================================

    def _predict_fraud_probability(
        self,
        request: RiskRequest,
    ) -> float:

        if not request.features:

            raise ValueError(
                "Risk request contains no "
                "model features."
            )

        try:

            probability = (
                self.model.predict_proba(
                    request.features
                )
            )

            fraud_probability = float(
                probability[0][1]
            )

        except Exception as e:

            logger.exception(
                "Fraud model prediction failed"
            )

            raise RuntimeError(
                "Unable to generate fraud "
                "probability."
            ) from e

        if not 0.0 <= fraud_probability <= 1.0:

            raise ValueError(
                "Fraud model returned an "
                "invalid probability."
            )

        return fraud_probability

    # ========================================================
    # RISK LEVEL
    # ========================================================

    def _get_risk_level(
        self,
        probability: float,
    ) -> RiskLevel:

        thresholds = (
            self.risk_thresholds
        )

        if probability <= thresholds.low_max:

            return RiskLevel.LOW

        if probability <= thresholds.medium_max:

            return RiskLevel.MEDIUM

        if probability <= thresholds.high_max:

            return RiskLevel.HIGH

        return RiskLevel.CRITICAL

    # ========================================================
    # GOVERNANCE DECISION
    # ========================================================

    def _get_decision(
        self,
        probability: float,
    ) -> RiskDecision:

        thresholds = (
            self.decision_thresholds
        )

        if probability >= (
            thresholds.block_threshold
        ):

            return RiskDecision.BLOCK

        if probability >= (
            thresholds.review_threshold
        ):

            return RiskDecision.REVIEW

        return RiskDecision.ALLOW

    # ========================================================
    # RULES
    # ========================================================

    def _get_triggered_rules(
        self,
        probability: float,
        risk_level: RiskLevel,
        decision: RiskDecision,
    ) -> list[str]:

        rules = []

        if risk_level == RiskLevel.LOW:

            rules.append(
                "low_fraud_probability"
            )

        elif risk_level == RiskLevel.MEDIUM:

            rules.append(
                "medium_fraud_probability"
            )

        elif risk_level == RiskLevel.HIGH:

            rules.append(
                "high_fraud_probability"
            )

        elif risk_level == RiskLevel.CRITICAL:

            rules.append(
                "critical_fraud_probability"
            )

        if decision == RiskDecision.REVIEW:

            rules.append(
                "manual_review_required"
            )

        if decision == RiskDecision.BLOCK:

            rules.append(
                "transaction_block_required"
            )

        return rules

    # ========================================================
    # EXPLANATION
    # ========================================================

    @staticmethod
    def _build_reason(
        probability: float,
        risk_level: RiskLevel,
        decision: RiskDecision,
        triggered_rules: list[str],
    ) -> str:

        return (
            f"Fraud probability is "
            f"{probability:.4f}. "
            f"Risk level is "
            f"{risk_level.value}. "
            f"Risk decision is "
            f"{decision.value}. "
            f"Triggered rules: "
            f"{', '.join(triggered_rules)}."
        )