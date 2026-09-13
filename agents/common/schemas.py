from pydantic import BaseModel
from typing import Optional, Dict, Any


class AgentRequest(BaseModel):
    agent_name: str
    user_query: str
    customer_id: Optional[int] = 1
    amount: Optional[float] = 0.0
    v_features: Optional[list] = None


class AgentResponse(BaseModel):
    agent_name: str
    response_text: str
    action_taken: str
    governance_status: str
    governance_explanation: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
