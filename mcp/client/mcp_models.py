from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MCPExecutionStatus(str, Enum):

    SUCCESS = "success"
    FAILED = "failed"
    DENIED = "denied"


class MCPToolRequest(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    action_id: str

    agent_id: str

    mcp_server: str

    mcp_tool: str

    arguments: dict[str, Any] = Field(
        default_factory=dict
    )

    amount: float | None = None


class MCPToolResponse(BaseModel):

    model_config = ConfigDict(
        extra="forbid"
    )

    request_id: str

    action_id: str

    status: MCPExecutionStatus

    result: Any = None

    error: str | None = None

    metadata: dict[str, Any] = Field(
        default_factory=dict
    )