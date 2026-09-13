import sys
from uuid import uuid4

from governance.approved_actions.approved_action_manager import (
    ApprovedActionError,
    ApprovedActionManager,
)

from mcp.client.mcp_exceptions import (
    MCPExecutionError,
    MCPServerNotFoundError,
    MCPToolNotFoundError,
    MCPVerificationError,
)

from mcp.client.mcp_models import (
    MCPExecutionStatus,
    MCPToolRequest,
    MCPToolResponse,
)

from mcp.client.mcp_server_registry import (
    MCPServerRegistry,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class MCPClient:

    def __init__(
        self,
        server_registry: MCPServerRegistry,
        approved_action_manager: (
            ApprovedActionManager
        ),
        audit_logger=None,
    ):

        self.server_registry = (
            server_registry
        )

        self.approved_action_manager = (
            approved_action_manager
        )

        self.audit_logger = (
            audit_logger
        )

        logger.info(
            "MCP client initialized"
        )

    # ========================================================
    # EXECUTE TOOL
    # ========================================================

    def execute(
        self,
        request: MCPToolRequest,
    ) -> MCPToolResponse:

        execution_request_id = str(
            uuid4()
        )

        logger.info(
            f"MCP execution requested: "
            f"request_id="
            f"{execution_request_id}, "
            f"agent={request.agent_id}, "
            f"server={request.mcp_server}, "
            f"tool={request.mcp_tool}"
        )

        try:

            # =================================================
            # STEP 1
            # VALIDATE APPROVED ACTION
            # =================================================

            approved_action = (
                self.approved_action_manager.validate(

                    action_id=request.action_id,

                    agent_id=request.agent_id,

                    mcp_server=request.mcp_server,

                    mcp_tool=request.mcp_tool,

                    amount=request.amount,
                )
            )

            # =================================================
            # STEP 2
            # SERVER EXISTS
            # =================================================

            if not self.server_registry.exists(
                request.mcp_server
            ):

                raise MCPServerNotFoundError(
                    f"MCP server not found: "
                    f"{request.mcp_server}"
                )

            server = (
                self.server_registry.get(
                    request.mcp_server
                )
            )

            # =================================================
            # STEP 3
            # TOOL EXISTS
            # =================================================

            available_tools = (
                server.list_tools()
            )

            if request.mcp_tool not in (
                available_tools
            ):

                raise MCPToolNotFoundError(
                    f"Tool '{request.mcp_tool}' "
                    f"is not exposed by "
                    f"'{request.mcp_server}'."
                )

            # =================================================
            # STEP 4
            # EXECUTE
            # =================================================

            result = server.execute(

                tool_name=request.mcp_tool,

                arguments=request.arguments,
            )

            # =================================================
            # STEP 5
            # CONSUME APPROVED ACTION
            # =================================================

            self.approved_action_manager.consume(
                request.action_id
            )

            # =================================================
            # STEP 6
            # AUDIT
            # =================================================

            self._audit_success(

                execution_request_id=(
                    execution_request_id
                ),

                request=request,

                result=result,
            )

            logger.info(
                f"MCP execution successful: "
                f"request_id="
                f"{execution_request_id}"
            )

            return MCPToolResponse(

                request_id=(
                    execution_request_id
                ),

                action_id=request.action_id,

                status=(
                    MCPExecutionStatus.SUCCESS
                ),

                result=result,

                metadata={
                    "mcp_server": (
                        request.mcp_server
                    ),
                    "mcp_tool": (
                        request.mcp_tool
                    ),
                },
            )

        except ApprovedActionError as e:

            logger.warning(
                f"MCP authorization rejected: "
                f"{e}"
            )

            self._audit_failure(

                execution_request_id,
                request,
                str(e),
            )

            return MCPToolResponse(

                request_id=(
                    execution_request_id
                ),

                action_id=request.action_id,

                status=(
                    MCPExecutionStatus.DENIED
                ),

                error=str(e),
            )

        except (
            MCPServerNotFoundError,
            MCPToolNotFoundError,
        ) as e:

            logger.error(
                f"MCP routing failure: {e}"
            )

            self._audit_failure(

                execution_request_id,
                request,
                str(e),
            )

            return MCPToolResponse(

                request_id=(
                    execution_request_id
                ),

                action_id=request.action_id,

                status=(
                    MCPExecutionStatus.FAILED
                ),

                error=str(e),
            )

        except Exception as e:

            logger.exception(
                "MCP tool execution failed"
            )

            self._audit_failure(

                execution_request_id,
                request,
                str(e),
            )

            return MCPToolResponse(

                request_id=(
                    execution_request_id
                ),

                action_id=request.action_id,

                status=(
                    MCPExecutionStatus.FAILED
                ),

                error=str(e),
            )

    # ========================================================
    # AUDIT SUCCESS
    # ========================================================

    def _audit_success(
        self,
        execution_request_id: str,
        request: MCPToolRequest,
        result,
    ):

        if self.audit_logger is None:

            return

        try:

            self.audit_logger.log_mcp_execution(

                request_id=(
                    execution_request_id
                ),

                action_id=(
                    request.action_id
                ),

                agent_id=(
                    request.agent_id
                ),

                mcp_server=(
                    request.mcp_server
                ),

                mcp_tool=(
                    request.mcp_tool
                ),

                status="success",

                metadata={
                    "result": str(result),
                },
            )

        except Exception:

            logger.exception(
                "Failed to audit MCP success"
            )

    # ========================================================
    # AUDIT FAILURE
    # ========================================================

    def _audit_failure(
        self,
        execution_request_id: str,
        request: MCPToolRequest,
        error: str,
    ):

        if self.audit_logger is None:

            return

        try:

            self.audit_logger.log_mcp_execution(

                request_id=(
                    execution_request_id
                ),

                action_id=(
                    request.action_id
                ),

                agent_id=(
                    request.agent_id
                ),

                mcp_server=(
                    request.mcp_server
                ),

                mcp_tool=(
                    request.mcp_tool
                ),

                status="failed",

                metadata={
                    "error": error,
                },
            )

        except Exception:

            logger.exception(
                "Failed to audit MCP failure"
            )