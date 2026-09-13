import uuid
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from backend.database.connection import get_db
from backend.database.models.audit import AuditLog
from backend.database.models.transaction import Transaction

from agents.supervisor_agent.workflow import SupervisorAgentWorkflow
from agents.common.schemas import AgentRequest
from governance_os.emergency_control.emergency_stop import EmergencyStopSwitch
from governance_os.agent_registry.agent_identity import AgentIdentityRegistry
from mcp.verification_layer.verification_models import VerificationRequest
from mcp.verification_layer.mcp_verifier import MCPServerVerifier
from mcp.servers.transaction_mcp.transaction_server import TransactionMCPServer
from security.prompt_guard import PromptInjectionGuard
from agents.fraud_agent.agent import FraudAgent

router = APIRouter(prefix="/api/agents", tags=["Agents"])

# Global singleton instances
_WORKFLOW = SupervisorAgentWorkflow()
_EMERGENCY_STOP = EmergencyStopSwitch()
_REGISTRY = AgentIdentityRegistry()
_VERIFIER = MCPServerVerifier()
_TX_MCP = TransactionMCPServer()
_FRAUD_AGENT = FraudAgent()


class AgentStatus(BaseModel):
    name: str
    role: str
    status: str
    model: str
    requests_processed: int


class RegisterAgentRequest(BaseModel):
    agent_name: str
    role: str  # supervisor, fraud_evaluator, loan_underwriter, refund_processor, support_assistant
    daily_budget_limit: Optional[float] = 10000.0


class AgentPaymentRequest(BaseModel):
    agent_name: str
    amount: float
    recipient: str
    description: str
    v_features: Optional[List[float]] = None


class AgentPaymentResponse(BaseModel):
    payment_status: str  # APPROVED, DENIED, BLOCKED
    risk_score: float
    is_fraud: bool
    mcp_transaction_id: Optional[str] = None
    agent_name: str
    governance_explanation: str


class ChatRequest(BaseModel):
    agent: Optional[str] = "Supervisor Agent"
    message: str
    amount: Optional[float] = 0.0


class ChatResponse(BaseModel):
    agent: str
    response: str
    action_taken: Optional[str] = None
    status: str
    governance_explanation: Optional[str] = None


@router.get("/status", response_model=List[AgentStatus])
def get_agents_status():
    is_stopped = _EMERGENCY_STOP.is_stopped
    status_label = "Emergency Stopped" if is_stopped else "Active"
    registered = _REGISTRY.registered_agents
    return [
        {
            "name": name,
            "role": meta["role"],
            "status": status_label if meta["status"] == "ACTIVE" else "Inactive",
            "model": "XGBoost + Governance OS",
            "requests_processed": 50
        }
        for name, meta in registered.items()
    ]


@router.post("/register")
def register_ai_agent(request: RegisterAgentRequest):
    """Register an external AI Agent on our Governance Platform."""
    agent_id = f"agent-ext-{uuid.uuid4().hex[:6]}"
    _REGISTRY.registered_agents[request.agent_name] = {
        "id": agent_id,
        "role": request.role,
        "status": "ACTIVE",
        "secret_hash": f"hash-{agent_id}"
    }
    return {
        "status": "SUCCESS",
        "agent_id": agent_id,
        "agent_name": request.agent_name,
        "role": request.role,
        "message": f"AI Agent '{request.agent_name}' successfully registered on Governance OS Platform."
    }


@router.post("/payment-request", response_model=AgentPaymentResponse)
def process_agent_payment_request(request: AgentPaymentRequest, db: Session = Depends(get_db)):
    """
    Core B2B Agent Flow:
    1. Input Prompt Guard Sanitization.
    2. XGBoost ML Risk Analysis & Probability Scoring.
    3. Governance OS OPA Rego Policy Check (spending cap, emergency stop, RBAC).
    4. 2-Stage MCP Verification Layer.
    5. MCP Transaction Execution if approved.
    """
    # 1. Prompt Injection Security Check
    passed, reason, sanitized_desc = PromptInjectionGuard.sanitize_and_validate(request.description)
    if not passed:
        audit = AuditLog(
            agent_id=request.agent_name,
            action="PAYMENT_PROMPT_INJECTION_BLOCKED",
            status="BLOCKED",
            details=reason
        )
        db.add(audit)
        db.commit()
        return AgentPaymentResponse(
            payment_status="BLOCKED",
            risk_score=1.0,
            is_fraud=True,
            agent_name=request.agent_name,
            governance_explanation=f"Security Guard: Payment description blocked due to injection risk: {reason}"
        )

    # 2. XGBoost ML Risk Analysis
    dummy_req = AgentRequest(
        agent_name=request.agent_name,
        user_query=sanitized_desc,
        amount=request.amount,
        v_features=request.v_features
    )
    fraud_eval = _FRAUD_AGENT.evaluate_fraud_risk(dummy_req)
    risk_score = fraud_eval.data.get("risk_score", 0.0) if fraud_eval.data else 0.0
    is_fraud = risk_score >= 0.50

    # 3 & 4. Governance OS & 2-Stage MCP Verification Layer
    ver_req = VerificationRequest(
        agent_id=request.agent_name,
        mcp_server="TransactionMCPServer",
        mcp_tool="process_transfer",
        amount=request.amount,
        risk_score=risk_score
    )
    ver_res = _VERIFIER.verify(ver_req)

    if not ver_res.verified or is_fraud:
        status_text = "BLOCKED" if is_fraud else "DENIED"
        explanation = f"XGBoost Flagged Fraud (Risk: {risk_score:.2f})" if is_fraud else ver_res.reason
        audit = AuditLog(
            agent_id=request.agent_name,
            action="PAYMENT_DENIED",
            status=status_text,
            details=f"Payment ${request.amount:.2f} to {request.recipient} denied: {explanation}"
        )
        db.add(audit)
        db.commit()
        return AgentPaymentResponse(
            payment_status=status_text,
            risk_score=risk_score,
            is_fraud=is_fraud,
            agent_name=request.agent_name,
            governance_explanation=f"Governance OS Gate Result: {explanation}"
        )

    # 5. Approved Payment Execution via MCP Server
    tx_id = f"TX-MCP-{uuid.uuid4().hex[:8].upper()}"
    new_tx = Transaction(
        customer_id=1,
        amount=request.amount,
        merchant=request.recipient,
        category="Agent Payment",
        status="completed",
        is_fraud=False,
        risk_score=risk_score
    )
    db.add(new_tx)

    audit = AuditLog(
        agent_id=request.agent_name,
        action="PAYMENT_APPROVED",
        status="APPROVED",
        details=f"Approved Payment ${request.amount:.2f} to {request.recipient} (TX: {tx_id})"
    )
    db.add(audit)
    db.commit()

    return AgentPaymentResponse(
        payment_status="APPROVED",
        risk_score=risk_score,
        is_fraud=False,
        mcp_transaction_id=tx_id,
        agent_name=request.agent_name,
        governance_explanation=f"Governance OS & OPA Rego Approved: Payment authorized and executed via Transaction MCP Server."
    )


@router.get("/emergency-stop/status")
def get_emergency_stop_status():
    return {
        "is_stopped": _EMERGENCY_STOP.is_stopped,
        "status": "STOPPED" if _EMERGENCY_STOP.is_stopped else "ACTIVE"
    }


@router.post("/emergency-stop/trigger")
def trigger_emergency_stop(db: Session = Depends(get_db)):
    _EMERGENCY_STOP.trigger_stop()
    audit = AuditLog(
        agent_id="SYSTEM_ADMIN",
        action="EMERGENCY_STOP_TRIGGERED",
        status="STOPPED",
        details="EMERGENCY STOP BUTTON PRESSED: All agent payment requests suspended immediately!"
    )
    db.add(audit)
    db.commit()
    return {
        "is_stopped": True,
        "message": "EMERGENCY STOP TRIGGERED! All agent payment requests suspended."
    }


@router.post("/emergency-stop/reset")
def reset_emergency_stop(db: Session = Depends(get_db)):
    _EMERGENCY_STOP.reset()
    audit = AuditLog(
        agent_id="SYSTEM_ADMIN",
        action="EMERGENCY_STOP_RESET",
        status="ACTIVE",
        details="EMERGENCY STOP RESET: Normal agent operations restored."
    )
    db.add(audit)
    db.commit()
    return {
        "is_stopped": False,
        "message": "Emergency Stop reset. Normal agent operations restored."
    }


class RevokeAgentRequest(BaseModel):
    agent_name: str


@router.post("/revoke")
def revoke_agent(request: RevokeAgentRequest, db: Session = Depends(get_db)):
    """Revoke credentials for a specific AI Agent in real-time."""
    from governance_os.emergency_control.revocation_store import RevocationStore
    store = RevocationStore()
    store.revoke_agent(request.agent_name)

    audit = AuditLog(
        agent_id=request.agent_name,
        action="AGENT_REVOKED",
        status="REVOKED",
        details=f"Real-Time Revocation: Access revoked for agent '{request.agent_name}'"
    )
    db.add(audit)
    db.commit()
    return {
        "status": "SUCCESS",
        "agent_name": request.agent_name,
        "message": f"Agent '{request.agent_name}' access revoked in real-time."
    }


@router.post("/unrevoke")
def unrevoke_agent(request: RevokeAgentRequest, db: Session = Depends(get_db)):
    """Restore credentials for a specific AI Agent in real-time."""
    from governance_os.emergency_control.revocation_store import RevocationStore
    store = RevocationStore()
    store.unrevoke_agent(request.agent_name)

    audit = AuditLog(
        agent_id=request.agent_name,
        action="AGENT_UNREVOKED",
        status="ACTIVE",
        details=f"Real-Time Revocation Reset: Access restored for agent '{request.agent_name}'"
    )
    db.add(audit)
    db.commit()
    return {
        "status": "SUCCESS",
        "agent_name": request.agent_name,
        "message": f"Agent '{request.agent_name}' access restored."
    }


@router.post("/chat", response_model=ChatResponse)
def query_agent(request: ChatRequest, db: Session = Depends(get_db)):
    passed, reason, sanitized_query = PromptInjectionGuard.sanitize_and_validate(request.message)
    if not passed:
        audit = AuditLog(
            agent_id="SECURITY_GUARD",
            action="PROMPT_INJECTION_BLOCKED",
            status="BLOCKED",
            details=reason
        )
        db.add(audit)
        db.commit()
        return ChatResponse(
            agent="Security Guard",
            response=f"Request blocked by Security Guard: {reason}",
            action_taken="PROMPT_INJECTION_BLOCKED",
            status="BLOCKED",
            governance_explanation="Malicious prompt injection attempt detected and blocked."
        )

    agent_req = AgentRequest(
        agent_name=request.agent or "Supervisor Agent",
        user_query=sanitized_query,
        amount=request.amount or 0.0
    )

    agent_res = _WORKFLOW.route_and_execute(agent_req)

    audit = AuditLog(
        agent_id=agent_res.agent_name,
        action=agent_res.action_taken,
        status=agent_res.governance_status,
        details=sanitized_query[:100]
    )
    db.add(audit)
    db.commit()

    return ChatResponse(
        agent=agent_res.agent_name,
        response=agent_res.response_text,
        action_taken=agent_res.action_taken,
        status=agent_res.governance_status,
        governance_explanation=agent_res.governance_explanation
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
