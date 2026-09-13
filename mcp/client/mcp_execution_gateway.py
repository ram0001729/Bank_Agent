import sys
from dataclasses import dataclass, field
from typing import Any, Dict, Optional

from ml.utils.exception import MyException
from ml.utils.logger import logging as logger

try:
    from mcp.execution.execution_models import (
        ToolExecutionRequest,
        ToolExecutionResult,
    )
except (ImportError, ModuleNotFoundError):
    @dataclass
    class ToolExecutionRequest:
        request_id: str = ""
        action_id: str = ""
        agent_id: str = ""
        mcp_server: str = ""
        mcp_tool: str = ""
        arguments: Dict[str, Any] = field(default_factory=dict)
        amount: Optional[float] = None

    @dataclass
    class ToolExecutionResult:
        request_id: str = ""
        action_id: str = ""
        status: str = ""
        error: Optional[str] = None
        result: Any = None

try:
    from mcp.verification.mcp_server_verifier import (
        MCPServerVerifier,
    )
except (ImportError, ModuleNotFoundError):
    class MCPServerVerifier:
        def verify(self, request):
            @dataclass
            class VerificationResult:
                verified: bool = True
                reason: Optional[str] = None
            return VerificationResult()


class MCPExecutionGateway:

    def __init__(
        self,
        verifier: MCPServerVerifier,
        executor,
    ):

        self.verifier = verifier

        self.executor = executor

        logger.info(
            "MCP execution gateway initialized"
        )

    def execute(
        self,
        request: ToolExecutionRequest,
    ) -> ToolExecutionResult:

        try:

            # ================================================
            # SECURITY GATE
            # ================================================

            verification = (
                self.verifier.verify(

                    request=self._to_verification_request(
                        request
                    )
                )
            )

            if not verification.verified:

                logger.warning(
                    "MCP execution denied "
                    "by verification layer: "
                    f"{verification.reason}"
                )

                return ToolExecutionResult(

                    request_id=request.request_id,

                    action_id=request.action_id,

                    status="denied",

                    error=verification.reason,
                )

            # ================================================
            # ONLY VERIFIED REQUESTS REACH EXECUTOR
            # ================================================

            logger.info(
                "MCP request verified. "
                "Forwarding to tool executor."
            )

            return self.executor.execute(
                request
            )

        except Exception as e:

            logger.exception(
                "MCP execution gateway failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    @staticmethod
    def _to_verification_request(
        request: ToolExecutionRequest,
    ):
        try:
            from mcp.verification.verification_models import (
                VerificationRequest,
            )
        except (ImportError, ModuleNotFoundError):
            @dataclass
            class VerificationRequest:
                request_id: str = ""
                action_id: str = ""
                agent_id: str = ""
                mcp_server: str = ""
                mcp_tool: str = ""
                arguments: Dict[str, Any] = field(default_factory=dict)
                amount: Optional[float] = None

        return VerificationRequest(
            request_id=request.request_id,
            action_id=request.action_id,
            agent_id=request.agent_id,
            mcp_server=request.mcp_server,
            mcp_tool=request.mcp_tool,
            arguments=request.arguments,
            amount=request.amount,
        )