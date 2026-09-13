import sys

from governance.decision.decision_models import (
    GovernanceEvaluation,
)

from governance.decision.governance_decision_engine import (
    GovernanceDecisionEngine,
)

from governance.explanation.explanation_engine import (
    ExplanationEngine,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class GovernanceService:

    def __init__(
        self,
        decision_engine: GovernanceDecisionEngine,
        explanation_engine: ExplanationEngine,
    ):

        self.decision_engine = (
            decision_engine
        )

        self.explanation_engine = (
            explanation_engine
        )

        logger.info(
            "Governance service initialized"
        )

    def evaluate(
        self,
        evaluation: GovernanceEvaluation,
    ):

        try:

            # =================================================
            # STEP 1
            # DETERMINISTIC DECISION
            # =================================================

            decision = (
                self.decision_engine.evaluate(
                    evaluation
                )
            )

            # =================================================
            # STEP 2
            # LLM EXPLANATION
            # =================================================

            explanation = (
                self.explanation_engine.explain(
                    decision
                )
            )

            return {
                "decision": decision,
                "explanation": explanation,
            }

        except Exception as e:

            logger.exception(
                "Governance service failed"
            )

            raise MyException(
                e,
                sys
            ) from e