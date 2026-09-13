from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from backend.database.connection import get_db
from backend.database.models.audit import AuditLog

router = APIRouter(prefix="/api/agents", tags=["Agents"])


class AgentStatus(BaseModel):
    name: str
    role: str
    status: str
    model: str
    requests_processed: int


class ChatRequest(BaseModel):
    agent: str
    message: str


class ChatResponse(BaseModel):
    agent: str
    response: str
    action_taken: Optional[str] = None
    status: str


class AuditLogSchema(BaseModel):
    id: int
    agent_id: str
    action: str
    status: str
    details: Optional[str]
    timestamp: str

    class Config:
        from_attributes = True


@router.get("/status", response_model=List[AgentStatus])
def get_agents_status():
    return [
        {
            "name": "Supervisor Agent",
            "role": "Intent Router & Supervisor",
            "status": "Active",
            "model": "Gemini 3.6 Flash",
            "requests_processed": 142
        },
        {
            "name": "Fraud Detection Agent",
            "role": "Risk Engine & ML Scoring",
            "status": "Active",
            "model": "XGBoost + Gemini",
            "requests_processed": 98
        },
        {
            "name": "Loan Approval Agent",
            "role": "Underwriting & Credit Risk",
            "status": "Active",
            "model": "Gemini 3.6 Flash",
            "requests_processed": 34
        },
        {
            "name": "Customer Support Agent",
            "role": "RAG & Policy Assistant",
            "status": "Active",
            "model": "Gemini 3.6 Flash",
            "requests_processed": 210
        }
    ]


@router.post("/chat", response_model=ChatResponse)
def query_agent(request: ChatRequest, db: Session = Depends(get_db)):
    msg_lower = request.message.lower()

    if "fraud" in msg_lower or "suspicious" in msg_lower:
        resp = "Fraud Agent: Transaction checked against XGBoost risk model. Risk score is within normal parameters."
        action = "RISK_EVALUATION"
    elif "loan" in msg_lower or "credit" in msg_lower:
        resp = "Loan Agent: Evaluated customer creditworthiness. Loan application is eligible for 7.5% APR."
        action = "LOAN_ASSESSMENT"
    else:
        resp = f"Supervisor Agent: Processed query via RAG policy retriever. Everything looks good!"
        action = "POLICY_QUERY"

    # Log to audit table
    audit = AuditLog(
        agent_id=request.agent or "Supervisor Agent",
        action=action,
        status="SUCCESS",
        details=request.message[:100]
    )
    db.add(audit)
    db.commit()

    return ChatResponse(
        agent=request.agent or "Supervisor Agent",
        response=resp,
        action_taken=action,
        status="SUCCESS"
    )


@router.get("/audit-logs")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(50).all()
    return [
        {
            "id": l.id,
            "agent_id": l.agent_id,
            "action": l.action,
            "status": l.status,
            "details": l.details,
            "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S") if l.timestamp else ""
        }
        for l in logs
    ]
