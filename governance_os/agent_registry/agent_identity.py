import hashlib
from typing import Dict, Any


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

    def verify_agent(self, agent_name: str) -> bool:
        return agent_name in self.registered_agents and self.registered_agents[agent_name]["status"] == "ACTIVE"

    def get_agent_metadata(self, agent_name: str) -> Dict[str, Any]:
        return self.registered_agents.get(agent_name, {})
