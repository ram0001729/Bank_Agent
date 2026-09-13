from agents.common.agent_base import BaseAgent
from agents.common.schemas import AgentRequest, AgentResponse
from mcp.verification_layer.verification_models import VerificationRequest
from mcp.servers.transaction_mcp.transaction_server import TransactionMCPServer
from rag.retrieval.retriever import PolicyRetriever


class RefundAgent(BaseAgent):
    def __init__(self):
        super().__init__("Refund Agent", "refund_processor")
        self.retriever = PolicyRetriever()
        self.tx_mcp = TransactionMCPServer()

    def process_refund_request(self, request: AgentRequest) -> AgentResponse:
        amount = request.amount or 150.0

        # RAG Search in Refund Policy PDF
        policy_res = self.retriever.get_relevant_policies("refund 30 days maximum limit dispute chargeback", top_k=2)

        # 2-Stage Verification check
        ver_req = VerificationRequest(
            agent_id=self.agent_name,
            mcp_server="TransactionMCPServer",
            mcp_tool="process_refund",
            amount=amount,
            risk_score=0.10
        )
        ver_res = self.verifier.verify(ver_req)

        self.log_langsmith_trace("process_refund_request", {"amount": amount}, {"verified": ver_res.verified})

        if not ver_res.verified:
            return AgentResponse(
                agent_name=self.agent_name,
                response_text=f"Refund Request Blocked by Governance OS: {ver_res.reason}",
                action_taken="REFUND_DENIED",
                governance_status="DENIED",
                governance_explanation=ver_res.explanation
            )

        mcp_data = self.tx_mcp.process_refund(101, amount)

        return AgentResponse(
            agent_name=self.agent_name,
            response_text=(
                f"Refund Agent Result: Successfully processed provisional refund of ${amount:,.2f} for Transaction #101.\n\n"
                f"Policy Citation (PDF RAG):\n{policy_res['context'][:280]}..."
            ),
            action_taken="REFUND_PROCESSED",
            governance_status="APPROVED",
            governance_explanation=ver_res.explanation,
            data=mcp_data
        )
