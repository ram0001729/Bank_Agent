from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, Optional
from uuid import uuid4


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    DENIED = "DENIED"


@dataclass
class VerificationRequest:
    agent_id: str
    mcp_server: str
    mcp_tool: str
    amount: Optional[float] = None
    risk_score: float = 0.0
    request_id: str = field(default_factory=lambda: str(uuid4()))
    action_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass
class VerificationResult:
    request_id: str
    action_id: str
    status: VerificationStatus
    verified: bool
    reason: str
    explanation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
