import hashlib
from typing import Dict, Any

from backend.database.models.agent import Agent


class AgentIdentityRegistry:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentIdentityRegistry, cls).__new__(cls)
            cls._instance.registered_agents = {
                "Supervisor Agent": {
                    "id": "agent-sup-001",
                    "role": "supervisor",
                    "status": "ACTIVE",
                    "secret_hash": hashlib.sha256(b"supervisor_token").hexdigest()
                },
                "Fraud Agent": {
                    "id": "agent-fraud-002",
                    "role": "fraud_evaluator",
                    "status": "ACTIVE",
                    "secret_hash": hashlib.sha256(b"fraud_token").hexdigest()
                },
                "Loan Agent": {
                    "id": "agent-loan-003",
                    "role": "loan_underwriter",
                    "status": "ACTIVE",
                    "secret_hash": hashlib.sha256(b"loan_token").hexdigest()
                },
                "Refund Agent": {
                    "id": "agent-refund-004",
                    "role": "refund_processor",
                    "status": "ACTIVE",
                    "secret_hash": hashlib.sha256(b"refund_token").hexdigest()
                },
                "Support Agent": {
                    "id": "agent-support-005",
                    "role": "support_assistant",
                    "status": "ACTIVE",
                    "secret_hash": hashlib.sha256(b"support_token").hexdigest()
                }
            }
        return cls._instance

    def verify_agent(self, agent_name: str, db=None) -> bool:
        if db is not None:
            agent = db.query(Agent).filter(Agent.agent_name == agent_name).first()
            return agent is not None and agent.status == "ACTIVE"
        return agent_name in self.registered_agents and self.registered_agents[agent_name]["status"] == "ACTIVE"

    def get_agent_metadata(self, agent_name: str, db=None) -> Dict[str, Any]:
        if db is not None:
            agent = db.query(Agent).filter(Agent.agent_name == agent_name).first()
            if agent is None:
                return {}
            return {
                "id": agent.agent_id,
                "role": agent.role,
                "status": agent.status,
                "daily_budget_limit": float(agent.daily_budget_limit),
            }
        return self.registered_agents.get(agent_name, {})
