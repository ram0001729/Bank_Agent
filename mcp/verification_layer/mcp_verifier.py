import sys

from governance.approved_actions.approved_action_manager import (
    ApprovedActionError,
    ApprovedActionManager,
)

from governance.emergency.emergency_stop import (
    AgentRevokedError,
    EmergencyStopController,
)

from mcp.verification.verification_exceptions import (
    AgentIdentityVerificationError,
    ApprovedActionVerificationError,
    BudgetVerificationError,
    EmergencyStopVerificationError,
    MCPVerificationError,
    PermissionVerificationError,
    PolicyVerificationError,
    RequestIntegrityError,
    RiskVerificationError,
)

from mcp.verification.verification_models import (
    VerificationRequest,
    VerificationResult,
    VerificationStatus,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class MCPServerVerifier:

    def __init__(
        self,
        agent_registry,
        permission_manager,
        approved_action_manager: (
            ApprovedActionManager
        ),
        emergency_stop: (
            EmergencyStopController
        ),
        policy_engine=None,
        risk_engine=None,
        budget_controller=None,
        audit_logger=None,
    ):

        self.agent_registry = (
            agent_registry
        )

        self.permission_manager = (
            permission_manager
        )

        self.approved_action_manager = (
            approved_action_manager
        )

        self.emergency_stop = (
            emergency_stop
        )

        self.policy_engine = (
            policy_engine
        )

        self.risk_engine = (
            risk_engine
        )

        self.budget_controller = (
            budget_controller
        )

        self.audit_logger = (
            audit_logger
        )

        logger.info(
            "MCP server verifier initialized"
        )

    # ========================================================
    # MAIN VERIFICATION
    # ========================================================

    def verify(
        self,
        request: VerificationRequest,
    ) -> VerificationResult:

        logger.info(
            "Starting MCP server verification: "
            f"request_id={request.request_id}, "
            f"agent_id={request.agent_id}, "
            f"tool={request.mcp_tool}"
        )

        try:

            # =================================================
            # 1. AGENT IDENTITY
            # =================================================

            self._verify_agent_identity(
                request.agent_id
            )

            # =================================================
            # 2. PERMISSION
            # =================================================

            self._verify_permission(
                request
            )

            # =================================================
            # 3. EMERGENCY STOP
            # =================================================

            self._verify_emergency_stop(
                request.agent_id
            )

            # =================================================
            # 4. APPROVED ACTION
            # =================================================

            approved_action = (
                self._verify_approved_action(
                    request
                )
            )

            # =================================================
            # 5. REQUEST INTEGRITY
            # =================================================

            self._verify_integrity(
                request,
                approved_action,
            )

            # =================================================
            # 6. POLICY
            # =================================================

            self._verify_policy(
                request,
                approved_action,
            )

            # =================================================
            # 7. RISK
            # =================================================

            self._verify_risk(
                request,
                approved_action,
            )

            # =================================================
            # 8. BUDGET
            # =================================================

            self._verify_budget(
                request,
                approved_action,
            )

            # =================================================
            # ALL CHECKS PASSED
            # =================================================

            result = VerificationResult(

                request_id=request.request_id,

                action_id=request.action_id,

                status=(
                    VerificationStatus.VERIFIED
                ),

                verified=True,

                reason=(
                    "All MCP server "
                    "verification checks passed."
                ),

                agent_verified=True,

                permission_verified=True,

                approved_action_verified=True,

                emergency_stop_verified=True,

                policy_verified=True,

                risk_verified=True,

                budget_verified=True,

                integrity_verified=True,
            )

            self._audit(
                request,
                result,
            )

            logger.info(
                "MCP server verification "
                "successful: "
                f"request_id={request.request_id}"
            )

            return result

        except MCPVerificationError as e:

            result = VerificationResult(

                request_id=request.request_id,

                action_id=request.action_id,

                status=(
                    VerificationStatus.DENIED
                ),

                verified=False,

                reason=str(e),
            )

            self._audit(
                request,
                result,
            )

            logger.warning(
                "MCP verification denied: "
                f"{e}"
            )

            return result

        except Exception as e:

            logger.exception(
                "Unexpected MCP verification failure"
            )

            raise MyException(
                e,
                sys
            ) from e

    # ========================================================
    # 1. AGENT IDENTITY
    # ========================================================

    def _verify_agent_identity(
        self,
        agent_id: str,
    ):

        try:

            identity = (
                self.agent_registry.get(
                    agent_id
                )
            )

            if identity is None:

                raise AgentIdentityVerificationError(
                    "Agent identity not found."
                )

        except Exception as e:

            if isinstance(
                e,
                AgentIdentityVerificationError
            ):
                raise

            raise AgentIdentityVerificationError(
                f"Agent identity verification "
                f"failed: {e}"
            ) from e

    # ========================================================
    # 2. PERMISSION
    # ========================================================

    def _verify_permission(
        self,
        request: VerificationRequest,
    ):

        if self.permission_manager is None:

            raise PermissionVerificationError(
                "Permission manager is not configured."
            )

        try:

            allowed = (
                self.permission_manager.check_permission(
                    agent_id=request.agent_id,
                    resource=request.mcp_server,
                    action=request.mcp_tool,
                )
            )

            if not allowed:

                raise PermissionVerificationError(
                    "Agent does not have permission "
                    "for this MCP tool."
                )

        except PermissionVerificationError:

            raise

        except Exception as e:

            raise PermissionVerificationError(
                f"Permission verification failed: "
                f"{e}"
            ) from e

    # ========================================================
    # 3. EMERGENCY STOP
    # ========================================================

    def _verify_emergency_stop(
        self,
        agent_id: str,
    ):

        try:

            self.emergency_stop.check_agent(
                agent_id
            )

        except AgentRevokedError as e:

            raise EmergencyStopVerificationError(
                str(e)
            ) from e

        except Exception as e:

            raise EmergencyStopVerificationError(
                f"Emergency stop verification "
                f"failed: {e}"
            ) from e

    # ========================================================
    # 4. APPROVED ACTION
    # ========================================================

    def _verify_approved_action(
        self,
        request: VerificationRequest,
    ):

        try:

            return (
                self.approved_action_manager.validate(

                    action_id=request.action_id,

                    agent_id=request.agent_id,

                    mcp_server=request.mcp_server,

                    mcp_tool=request.mcp_tool,

                    amount=request.amount,
                )
            )

        except ApprovedActionError as e:

            raise ApprovedActionVerificationError(
                str(e)
            ) from e

    # ========================================================
    # 5. REQUEST INTEGRITY
    # ========================================================

    def _verify_integrity(
        self,
        request: VerificationRequest,
        approved_action,
    ):

        if (
            approved_action.mcp_server
            != request.mcp_server
        ):

            raise RequestIntegrityError(
                "MCP server does not match "
                "approved action."
            )

        if (
            approved_action.mcp_tool
            != request.mcp_tool
        ):

            raise RequestIntegrityError(
                "MCP tool does not match "
                "approved action."
            )

        if (
            request.amount is not None
            and approved_action.amount is not None
            and request.amount
            > approved_action.amount
        ):

            raise RequestIntegrityError(
                "Requested amount exceeds "
                "approved amount."
            )

    # ========================================================
    # 6. POLICY
    # ========================================================

    def _verify_policy(
        self,
        request,
        approved_action,
    ):

        # Policy engine is optional during
        # early development.

        if self.policy_engine is None:

            logger.warning(
                "Policy engine not configured "
                "for MCP verification."
            )

            return

        try:

            # Your actual policy engine API
            # should be connected here.

            result = (
                self.policy_engine.evaluate(
                    agent_id=request.agent_id,
                    action=request.mcp_tool,
                    resource=request.mcp_server,
                    arguments=request.arguments,
                )
            )

            if not result.allowed:

                raise PolicyVerificationError(
                    "Policy engine denied "
                    "MCP operation."
                )

        except PolicyVerificationError:

            raise

        except Exception as e:

            raise PolicyVerificationError(
                f"Policy verification failed: "
                f"{e}"
            ) from e

    # ========================================================
    # 7. RISK
    # ========================================================

    def _verify_risk(
        self,
        request,
        approved_action,
    ):

        if self.risk_engine is None:

            logger.warning(
                "Risk engine not configured "
                "for MCP verification."
            )

            return

        try:

            result = (
                self.risk_engine.evaluate(
                    agent_id=request.agent_id,
                    action=request.mcp_tool,
                    amount=request.amount,
                    arguments=request.arguments,
                )
            )

            if not result.allowed:

                raise RiskVerificationError(
                    "Risk engine denied "
                    "MCP operation."
                )

        except RiskVerificationError:

            raise

        except Exception as e:

            raise RiskVerificationError(
                f"Risk verification failed: "
                f"{e}"
            ) from e

    # ========================================================
    # 8. BUDGET
    # ========================================================

    def _verify_budget(
        self,
        request,
        approved_action,
    ):

        if self.budget_controller is None:

            logger.warning(
                "Budget controller not configured "
                "for MCP verification."
            )

            return

        if request.amount is None:

            return

        try:

            result = (
                self.budget_controller.check_budget(
                    agent_id=request.agent_id,
                    amount=request.amount,
                )
            )

            if not result.allowed:

                raise BudgetVerificationError(
                    "Budget controller denied "
                    "MCP operation."
                )

        except BudgetVerificationError:

            raise

        except Exception as e:

            raise BudgetVerificationError(
                f"Budget verification failed: "
                f"{e}"
            ) from e

    # ========================================================
    # AUDIT
    # ========================================================

    def _audit(
        self,
        request,
        result,
    ):

        if self.audit_logger is None:

            return

        try:

            self.audit_logger.log_mcp_verification(

                request_id=request.request_id,

                action_id=request.action_id,

                agent_id=request.agent_id,

                mcp_server=request.mcp_server,

                mcp_tool=request.mcp_tool,

                status=result.status.value,

                reason=result.reason,
            )

        except Exception:

            logger.exception(
                "Failed to audit MCP verification"
            )