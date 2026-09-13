import sys

from governance.decision.decision_models import (
    ComponentDecision,
    GovernanceDecision,
    GovernanceDecisionResult,
    GovernanceEvaluation,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class GovernanceDecisionEngine:

    def __init__(
        self,
        audit_logger=None,
    ):

        self.audit_logger = audit_logger

        logger.info(
            "Governance decision engine initialized"
        )

    # ========================================================
    # MAIN DECISION
    # ========================================================

    def evaluate(
        self,
        evaluation: GovernanceEvaluation,
    ) -> GovernanceDecisionResult:

        try:

            logger.info(
                f"Governance evaluation started: "
                f"request_id="
                f"{evaluation.request_id}"
            )

            blocking_components = []

            escalation_components = []

            # ------------------------------------------------
            # OPA
            # ------------------------------------------------

            self._check_component(
                name="opa",
                component=evaluation.opa,
                blocking_components=(
                    blocking_components
                ),
                escalation_components=(
                    escalation_components
                ),
            )

            # ------------------------------------------------
            # POLICY
            # ------------------------------------------------

            self._check_component(
                name="policy",
                component=evaluation.policy,
                blocking_components=(
                    blocking_components
                ),
                escalation_components=(
                    escalation_components
                ),
            )

            # ------------------------------------------------
            # RISK
            # ------------------------------------------------

            self._check_component(
                name="risk",
                component=evaluation.risk,
                blocking_components=(
                    blocking_components
                ),
                escalation_components=(
                    escalation_components
                ),
            )

            # ------------------------------------------------
            # BUDGET
            # ------------------------------------------------

            self._check_component(
                name="budget",
                component=evaluation.budget,
                blocking_components=(
                    blocking_components
                ),
                escalation_components=(
                    escalation_components
                ),
            )

            # ------------------------------------------------
            # FINAL DECISION
            # ------------------------------------------------

            if blocking_components:

                decision = (
                    GovernanceDecision.DENY
                )

                reason = (
                    "Governance request denied "
                    "because one or more control "
                    "components rejected the request."
                )

            elif escalation_components:

                decision = (
                    GovernanceDecision.ESCALATE
                )

                reason = (
                    "Governance request requires "
                    "additional review because one "
                    "or more control components "
                    "require escalation."
                )

            else:

                decision = (
                    GovernanceDecision.ALLOW
                )

                reason = (
                    "All governance control "
                    "components approved the request."
                )

            result = GovernanceDecisionResult(

                request_id=evaluation.request_id,

                agent_id=evaluation.agent_id,

                agent_name=evaluation.agent_name,

                agent_type=evaluation.agent_type,

                user_id=evaluation.user_id,

                action=evaluation.action,

                resource=evaluation.resource,

                amount=evaluation.amount,

                currency=evaluation.currency,

                decision=decision,

                reason=reason,

                blocking_components=(
                    blocking_components
                ),

                escalation_components=(
                    escalation_components
                ),

                opa=evaluation.opa,

                policy=evaluation.policy,

                risk=evaluation.risk,

                budget=evaluation.budget,

                metadata={
                    "decision_engine": (
                        "governance_decision_engine"
                    )
                },
            )

            logger.info(
                f"Governance decision completed: "
                f"request_id="
                f"{evaluation.request_id}, "
                f"decision="
                f"{decision.value}"
            )

            self._audit(
                result
            )

            return result

        except Exception as e:

            logger.exception(
                "Governance decision evaluation failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # COMPONENT CHECK
    # ========================================================

    @staticmethod
    def _check_component(
        name: str,
        component: ComponentDecision,
        blocking_components: list[str],
        escalation_components: list[str],
    ):

        decision = (
            component.decision.lower()
        )

        # -----------------------------------------------
        # DENY / BLOCK
        # -----------------------------------------------

        if decision in {
            "deny",
            "blocked",
            "block",
            "rejected",
            "reject",
        }:

            blocking_components.append(
                name
            )

            return

        # -----------------------------------------------
        # ESCALATE / REVIEW
        # -----------------------------------------------

        if decision in {
            "escalate",
            "review",
            "manual_review",
            "warning",
        }:

            escalation_components.append(
                name
            )

            return

        # -----------------------------------------------
        # ALLOW
        # -----------------------------------------------

        if decision in {
            "allow",
            "allowed",
            "approved",
            "approve",
        }:

            return

        # -----------------------------------------------
        # UNKNOWN DECISION
        # -----------------------------------------------

        # Fail closed.
        blocking_components.append(
            name
        )

        logger.error(
            f"Unknown governance decision "
            f"from {name}: {decision}"
        )

    # ========================================================
    # AUDIT
    # ========================================================

    def _audit(
        self,
        result: GovernanceDecisionResult,
    ):

        if self.audit_logger is None:

            return

        try:

            self.audit_logger.log_governance_decision(

                request_id=result.request_id,

                agent_id=result.agent_id,

                agent_name=result.agent_name,

                decision=result.decision.value,

                reason=result.reason,

                action=result.action,

                resource=result.resource,

                user_id=result.user_id,

                amount=result.amount,

                currency=result.currency,

                metadata={
                    "blocking_components": (
                        result.blocking_components
                    ),
                    "escalation_components": (
                        result.escalation_components
                    ),
                },
            )

        except Exception:

            # Audit failure must never silently
            # change the governance decision.
            logger.exception(
                "Failed to audit governance decision"
            )