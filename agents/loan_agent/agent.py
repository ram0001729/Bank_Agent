from agents.common.agent_base import BaseAgent
from agents.common.schemas import AgentRequest, AgentResponse
from mcp.verification_layer.verification_models import VerificationRequest
from mcp.servers.loan_mcp.loan_server import LoanMCPServer
from rag.retrieval.retriever import PolicyRetriever


class LoanAgent(BaseAgent):
    def __init__(self):
        super().__init__("Loan Agent", "loan_underwriter")
        self.retriever = PolicyRetriever()
        self.loan_mcp = LoanMCPServer()

    def process_loan_request(self, request: AgentRequest) -> AgentResponse:
        amount = request.amount or 10000.0

        # RAG Search in Loan Policy PDF
        policy_res = self.retriever.get_relevant_policies("loan eligibility credit score interest rate limit", top_k=2)

        # 2-Stage Verification check
        ver_req = VerificationRequest(
            agent_id=self.agent_name,
            mcp_server="LoanMCPServer",
            mcp_tool="approve_loan",
            amount=amount,
            risk_score=0.15
        )
        ver_res = self.verifier.verify(ver_req)

        self.log_langsmith_trace("process_loan_request", {"amount": amount}, {"verified": ver_res.verified})

        if not ver_res.verified:
            return AgentResponse(
                agent_name=self.agent_name,
                response_text=f"Loan Underwriting Result: Denied by Governance OS. Reason: {ver_res.reason}",
                action_taken="LOAN_DENIED",
                governance_status="DENIED",
                governance_explanation=ver_res.explanation
            )

        mcp_data = self.loan_mcp.approve_loan_application(request.customer_id or 1, amount)

        return AgentResponse(
            agent_name=self.agent_name,
            response_text=(
                f"Loan Agent Underwriting Result: Approved personal loan of ${amount:,.2f} at 7.5% APR!\n\n"
                f"Relevant Policy Reference (PDF RAG):\n{policy_res['context'][:300]}..."
            ),
            action_taken="LOAN_APPROVED",
            governance_status="APPROVED",
            governance_explanation=ver_res.explanation,
            data=mcp_data
        )
