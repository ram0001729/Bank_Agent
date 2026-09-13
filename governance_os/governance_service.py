from typing import Dict, Any
from governance_os.agent_registry.agent_identity import AgentIdentityRegistry
from governance_os.permission_manager.permission_manager import PermissionManager
from governance_os.policy_engine.policy_engine import PolicyEngine
from governance_os.budget_controller.budget_controller import BudgetController
from governance_os.explanation_engine.explanation_engine import ExplanationEngine
from governance_os.emergency_control.emergency_stop import EmergencyStopSwitch
from governance_os.emergency_control.revocation_store import RevocationStore


class GovernanceOSService:
    def __init__(self, db=None):
        self.db = db
        self.registry = AgentIdentityRegistry()
        self.permission_manager = PermissionManager()
        self.policy_engine = PolicyEngine()
        self.budget_controller = BudgetController()
        self.explanation_engine = ExplanationEngine()
        self.emergency_switch = EmergencyStopSwitch()
        self.revocation_store = RevocationStore()

    def evaluate_governance(
        self,
        agent_name: str,
        action: str,
        amount: float = 0.0,
        risk_score: float = 0.0
    ) -> Dict[str, Any]:
        # 1. Emergency Stop Check (Fleet-wide Halt)
        if not self.emergency_switch.check_active():
            return {
                "allowed": False,
                "reason": "EMERGENCY_STOP_ACTIVE: All agent operations suspended by fleet circuit breaker.",
                "explanation": "Operations suspended by administrator emergency kill-switch."
            }

        # 2. Real-Time Per-Agent Revocation Check
        if self.revocation_store.is_revoked(agent_name):
            return {
                "allowed": False,
                "reason": f"AGENT_REVOKED: Agent '{agent_name}' access has been revoked by Real-Time Revocation Control.",
                "explanation": "Agent credentials revoked by administrator."
            }

        # 3. Agent Identity Verification
        if not self.registry.verify_agent(agent_name, db=self.db):
            return {
                "allowed": False,
                "reason": f"UNREGISTERED_AGENT: Agent '{agent_name}' not registered in Identity Registry.",
                "explanation": "Agent cryptographic identity verification failed."
            }

        agent_meta = self.registry.get_agent_metadata(agent_name, db=self.db)

        # 4. Permission Manager Check (Granular RBAC/ABAC Permissions)
        if not self.permission_manager.check_permission(agent_meta.get("role", ""), action):
            return {
                "allowed": False,
                "reason": f"PERMISSION_DENIED: Role '{agent_meta.get('role')}' unauthorized for action '{action}'.",
                "explanation": "RBAC permission check failed."
            }

        # 5. Policy Engine Check (OPA Rego Rules)
        allowed_policy, policy_reason = self.policy_engine.evaluate_policy(
            action,
            amount,
            risk_score,
            role=agent_meta.get("role", "supervisor"),
            agent_budget_limit=agent_meta.get("daily_budget_limit", 10000.0),
        )
        if not allowed_policy:
            explanation = self.explanation_engine.generate_explanation(action, False, policy_reason, risk_score)
            return {
                "allowed": False,
                "reason": policy_reason,
                "explanation": explanation
            }

        # 6. Dynamic Spend Caps (Budget Controller)
        if amount > 0 and not self.budget_controller.check_and_reserve_budget(amount):
            return {
                "allowed": False,
                "reason": "BUDGET_CAP_EXCEEDED: Daily cumulative spending cap exceeded.",
                "explanation": "Action blocked by Budget Controller."
            }

        # 7. Action Approval & Rationale Explanation
        explanation = self.explanation_engine.generate_explanation(action, True, "All governance safety gates passed", risk_score)
        return {
            "allowed": True,
            "reason": "Governance OS approved action",
            "explanation": explanation
        }
