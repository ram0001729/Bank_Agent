from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ToolExecutionRequest:
    request_id: str = ""
    action_id: str = ""
    agent_id: str = ""
    mcp_server: str = ""
    mcp_tool: str = ""
    arguments: Dict[str, Any] = field(default_factory=dict)
    amount: Optional[float] = None
    risk_score: Optional[float] = 0.0


@dataclass
class ToolExecutionResult:
    request_id: str = ""
    action_id: str = ""
    status: str = ""
    error: Optional[str] = None
    result: Any = None
