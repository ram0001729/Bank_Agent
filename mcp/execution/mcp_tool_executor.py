import sys
from typing import Any

from mcp.client.mcp_server_registry import (
    MCPServerRegistry,
)

from mcp.execution.execution_models import (
    ToolExecutionRequest,
    ToolExecutionResult,
    ToolExecutionStatus,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class MCPToolExecutor:

    def __init__(
        self,
        server_registry: MCPServerRegistry,
        audit_logger=None,
    ):

        self.server_registry = (
            server_registry
        )

        self.audit_logger = (
            audit_logger
        )

        logger.info(
            "MCP tool executor initialized"
        )

    # ========================================================
    # EXECUTE
    # ========================================================

    def execute(
        self,
        request: ToolExecutionRequest,
    ) -> ToolExecutionResult:

        try:

            logger.info(
                "Starting MCP tool execution: "
                f"request_id={request.request_id}, "
                f"action_id={request.action_id}, "
                f"server={request.mcp_server}, "
                f"tool={request.mcp_tool}"
            )

            # ------------------------------------------------
            # SERVER LOOKUP
            # ------------------------------------------------

            if not self.server_registry.exists(
                request.mcp_server
            ):

                raise ValueError(
                    f"MCP server not found: "
                    f"{request.mcp_server}"
                )

            server = (
                self.server_registry.get(
                    request.mcp_server
                )
            )

            # ------------------------------------------------
            # TOOL LOOKUP
            # ------------------------------------------------

            available_tools = (
                server.list_tools()
            )

            if request.mcp_tool not in (
                available_tools
            ):

                raise ValueError(
                    f"MCP tool not available: "
                    f"{request.mcp_tool}"
                )

            # ------------------------------------------------
            # EXECUTE TOOL
            # ------------------------------------------------

            result = server.execute(

                tool_name=request.mcp_tool,

                arguments=request.arguments,
            )

            logger.info(
                "MCP tool execution completed: "
                f"request_id={request.request_id}, "
                f"tool={request.mcp_tool}"
            )

            self._audit_success(
                request,
                result
            )

            return ToolExecutionResult(

                request_id=request.request_id,

                action_id=request.action_id,

                status=(
                    ToolExecutionStatus.SUCCESS
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

        except Exception as e:

            logger.exception(
                "MCP tool execution failed"
            )

            self._audit_failure(
                request,
                str(e)
            )

            return ToolExecutionResult(

                request_id=request.request_id,

                action_id=request.action_id,

                status=(
                    ToolExecutionStatus.FAILED
                ),

                error=str(e),

                metadata={
                    "mcp_server": (
                        request.mcp_server
                    ),

                    "mcp_tool": (
                        request.mcp_tool
                    ),
                },
            )

    # ========================================================
    # AUDIT SUCCESS
    # ========================================================

    def _audit_success(
        self,
        request: ToolExecutionRequest,
        result: Any,
    ):

        if self.audit_logger is None:

            return

        try:

            self.audit_logger.log_mcp_execution(

                request_id=request.request_id,

                action_id=request.action_id,

                agent_id=request.agent_id,

                mcp_server=request.mcp_server,

                mcp_tool=request.mcp_tool,

                status="success",

                metadata={
                    "result": str(result),
                },
            )

        except Exception:

            logger.exception(
                "Failed to audit MCP execution"
            )

    # ========================================================
    # AUDIT FAILURE
    # ========================================================

    def _audit_failure(
        self,
        request: ToolExecutionRequest,
        error: str,
    ):

        if self.audit_logger is None:

            return

        try:

            self.audit_logger.log_mcp_execution(

                request_id=request.request_id,

                action_id=request.action_id,

                agent_id=request.agent_id,

                mcp_server=request.mcp_server,

                mcp_tool=request.mcp_tool,

                status="failed",

                metadata={
                    "error": error,
                },
            )

        except Exception:

            logger.exception(
                "Failed to audit MCP failure"
            )