from agents.common.agent_base import BaseAgent
from agents.common.schemas import AgentRequest, AgentResponse
from agents.fraud_agent.agent import FraudAgent
from agents.loan_agent.agent import LoanAgent
from agents.refund_agent.agent import RefundAgent
from agents.support_agent.agent import SupportAgent


class SupervisorAgentWorkflow(BaseAgent):
    def __init__(self):
        super().__init__("Supervisor Agent", "supervisor")
        self.fraud_agent = FraudAgent()
        self.loan_agent = LoanAgent()
        self.refund_agent = RefundAgent()
        self.support_agent = SupportAgent()

    def route_and_execute(self, request: AgentRequest) -> AgentResponse:
        query_lower = request.user_query.lower()

        # Intent Detection & Routing Logic
        if "fraud" in query_lower or "suspicious" in query_lower or "unauthorized" in query_lower or "risk" in query_lower:
            target_agent = "Fraud Agent"
            resp = self.fraud_agent.evaluate_fraud_risk(request)

        elif "loan" in query_lower or "mortgage" in query_lower or "credit score" in query_lower or "apr" in query_lower:
            target_agent = "Loan Agent"
            resp = self.loan_agent.process_loan_request(request)

        elif "refund" in query_lower or "chargeback" in query_lower or "dispute" in query_lower:
            target_agent = "Refund Agent"
            resp = self.refund_agent.process_refund_request(request)

        else:
            target_agent = "Support Agent"
            resp = self.support_agent.answer_support_query(request)

        self.log_langsmith_trace("route_and_execute", {"query": request.user_query}, {"routed_to": target_agent, "status": resp.governance_status})
        return resp
