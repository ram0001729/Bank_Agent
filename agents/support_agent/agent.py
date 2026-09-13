from agents.common.agent_base import BaseAgent
from agents.common.schemas import AgentRequest, AgentResponse
from rag.retrieval.retriever import PolicyRetriever


class SupportAgent(BaseAgent):
    def __init__(self):
        super().__init__("Support Agent", "support_assistant")
        self.retriever = PolicyRetriever()

    def answer_support_query(self, request: AgentRequest) -> AgentResponse:
        policy_res = self.retriever.get_relevant_policies(request.user_query, top_k=3)

        self.log_langsmith_trace("answer_support_query", {"query": request.user_query}, {"results_count": len(policy_res['results'])})

        response_text = (
            f"Customer Support Assistant: Here is the information retrieved from our official bank policy documents:\n\n"
            f"{policy_res['context']}\n\n"
            f"If you have further questions or require agent escalation, please let me know!"
        )

        return AgentResponse(
            agent_name=self.agent_name,
            response_text=response_text,
            action_taken="POLICY_QA",
            governance_status="APPROVED",
            governance_explanation="Policy query executed via RAG Vector Search.",
            data={"sources": [r["source"] for r in policy_res["results"]]}
        )
