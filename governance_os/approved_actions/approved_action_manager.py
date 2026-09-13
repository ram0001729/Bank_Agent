import sys
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from governance.approved_actions.action_models import (
    ActionStatus,
    ApprovedAction,
)

from governance.approved_actions.action_store import (
    ApprovedActionStore,
)

from governance.decision.decision_models import (
    GovernanceDecisionResult,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class ApprovedActionError(
    RuntimeError
):
    pass


class ApprovedActionManager:

    def __init__(
        self,
        store: ApprovedActionStore | None = None,
        emergency_stop=None,
        audit_logger=None,
        ttl_seconds: int = 60,
    ):

        self.store = (
            store
            or ApprovedActionStore()
        )

        self.emergency_stop = (
            emergency_stop
        )

        self.audit_logger = (
            audit_logger
        )

        self.ttl_seconds = (
            ttl_seconds
        )

        logger.info(
            "Approved action manager initialized"
        )

    # ========================================================
    # ISSUE APPROVED ACTION
    # ========================================================

    def issue(
        self,
        decision: GovernanceDecisionResult,
        mcp_server: str,
        mcp_tool: str,
    ) -> ApprovedAction:

        try:

            # ------------------------------------------------
            # Only ALLOW can create approved action
            # ------------------------------------------------

            if decision.decision.value != "allow":

                raise ApprovedActionError(
                    "Approved action cannot be "
                    "created for a non-ALLOW decision."
                )

            # ------------------------------------------------
            # Emergency stop check
            # ------------------------------------------------

            if self.emergency_stop is not None:

                self.emergency_stop.check_agent(
                    decision.agent_id
                )

            now = datetime.now(
                timezone.utc
            )

            expires_at = (
                now
                + timedelta(
                    seconds=self.ttl_seconds
                )
            )

            action_id = str(
                uuid4()
            )

            approved_action = ApprovedAction(

                action_id=action_id,

                request_id=(
                    decision.request_id
                ),

                agent_id=(
                    decision.agent_id
                ),

                agent_name=(
                    decision.agent_name
                ),

                agent_type=(
                    decision.agent_type
                ),

                user_id=(
                    decision.user_id
                ),

                action=(
                    decision.action
                ),

                resource=(
                    decision.resource
                ),

                mcp_server=mcp_server,

                mcp_tool=mcp_tool,

                amount=(
                    decision.amount
                ),

                currency=(
                    decision.currency
                ),

                issued_at=now,

                expires_at=expires_at,

                governance_decision="allow",

                governance_snapshot={
                    "opa": (
                        decision.opa.model_dump()
                    ),

                    "policy": (
                        decision.policy.model_dump()
                    ),

                    "risk": (
                        decision.risk.model_dump()
                    ),

                    "budget": (
                        decision.budget.model_dump()
                    ),
                },
            )

            self.store.save(
                approved_action
            )

            logger.info(
                f"Approved action issued: "
                f"action_id={action_id}, "
                f"agent="
                f"{decision.agent_name}, "
                f"tool={mcp_tool}"
            )

            return approved_action

        except ApprovedActionError:

            raise

        except Exception as e:

            logger.exception(
                "Failed to issue approved action"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # VALIDATE ACTION
    # ========================================================

    def validate(
        self,
        action_id: str,
        agent_id: str,
        mcp_server: str,
        mcp_tool: str,
        amount: float | None = None,
    ) -> ApprovedAction:

        try:

            # ------------------------------------------------
            # Emergency stop
            # ------------------------------------------------

            if self.emergency_stop is not None:

                self.emergency_stop.check_agent(
                    agent_id
                )

            # ------------------------------------------------
            # Retrieve capability
            # ------------------------------------------------

            action = self.store.get(
                action_id
            )

            if action is None:

                raise ApprovedActionError(
                    "Approved action does not exist."
                )

            # ------------------------------------------------
            # Status
            # ------------------------------------------------

            if action.status != (
                ActionStatus.APPROVED
            ):

                raise ApprovedActionError(
                    f"Approved action is "
                    f"{action.status.value}."
                )

            # ------------------------------------------------
            # Expiration
            # ------------------------------------------------

            now = datetime.now(
                timezone.utc
            )

            if now >= action.expires_at:

                action.status = (
                    ActionStatus.EXPIRED
                )

                self.store.update(
                    action
                )

                raise ApprovedActionError(
                    "Approved action has expired."
                )

            # ------------------------------------------------
            # Agent binding
            # ------------------------------------------------

            if action.agent_id != agent_id:

                raise ApprovedActionError(
                    "Approved action does not "
                    "belong to this agent."
                )

            # ------------------------------------------------
            # MCP server binding
            # ------------------------------------------------

            if action.mcp_server != mcp_server:

                raise ApprovedActionError(
                    "Approved action is not "
                    "authorized for this MCP server."
                )

            # ------------------------------------------------
            # MCP tool binding
            # ------------------------------------------------

            if action.mcp_tool != mcp_tool:

                raise ApprovedActionError(
                    "Approved action is not "
                    "authorized for this MCP tool."
                )

            # ------------------------------------------------
            # Amount binding
            # ------------------------------------------------

            if (
                amount is not None
                and action.amount is not None
                and amount > action.amount
            ):

                raise ApprovedActionError(
                    "Requested amount exceeds "
                    "approved amount."
                )

            logger.info(
                f"Approved action validated: "
                f"action_id={action_id}"
            )

            return action

        except ApprovedActionError:

            raise

        except Exception as e:

            logger.exception(
                "Approved action validation failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # CONSUME ACTION
    # ========================================================

    def consume(
        self,
        action_id: str,
    ) -> None:

        try:

            action = self.store.get(
                action_id
            )

            if action is None:

                raise ApprovedActionError(
                    "Approved action not found."
                )

            if action.status != (
                ActionStatus.APPROVED
            ):

                raise ApprovedActionError(
                    "Only an approved action "
                    "can be consumed."
                )

            action.status = (
                ActionStatus.CONSUMED
            )

            action.consumed_at = (
                datetime.now(
                    timezone.utc
                )
            )

            self.store.update(
                action
            )

            logger.info(
                f"Approved action consumed: "
                f"action_id={action_id}"
            )

        except ApprovedActionError:

            raise

        except Exception as e:

            logger.exception(
                "Failed to consume approved action"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # REVOKE ACTION
    # ========================================================

    def revoke(
        self,
        action_id: str,
    ) -> None:

        self.store.revoke(
            action_id
        )