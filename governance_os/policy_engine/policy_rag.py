import sys

from governance.policy.policy_models import PolicyRequest
from rag.schemas import RAGResult

from ml.utils.exception import MyException
from ml.utils.logger import logger


class PolicyRAG:

    def __init__(
        self,
        retriever,
        reranker,
        top_k_retrieval: int = 10,
        top_k_rerank: int = 5,
    ):

        self.retriever = retriever
        self.reranker = reranker

        self.top_k_retrieval = (
            top_k_retrieval
        )

        self.top_k_rerank = (
            top_k_rerank
        )

        logger.info(
            "Policy RAG initialized"
        )

    def build_query(
        self,
        request: PolicyRequest
    ) -> str:

        context = " ".join(
            f"{key}: {value}"
            for key, value
            in request.context.items()
        )

        query_parts = [
            f"banking policy",
            f"agent type: {request.agent_type}",
            f"action: {request.action}",
            f"resource: {request.resource}",
        ]

        if request.amount is not None:

            query_parts.append(
                f"amount: {request.amount}"
            )

        if request.risk_level:

            query_parts.append(
                f"risk level: {request.risk_level}"
            )

        if context:

            query_parts.append(
                f"context: {context}"
            )

        return " ".join(query_parts)

    def retrieve_policy(
        self,
        request: PolicyRequest,
        query_filter=None,
    ) -> RAGResult:

        try:

            query = self.build_query(
                request
            )

            logger.info(
                f"Policy RAG query: {query}"
            )

            candidates = (
                self.retriever.retrieve(
                    query=query,
                    top_k=self.top_k_retrieval,
                    query_filter=query_filter,
                )
            )

            reranked = (
                self.reranker.rerank(
                    query=query,
                    documents=candidates,
                    top_k=self.top_k_rerank,
                )
            )

            context = (
                self._build_context(
                    reranked
                )
            )

            logger.info(
                f"Policy RAG retrieved "
                f"{len(reranked)} policy chunks"
            )

            return RAGResult(
                query=query,
                results=reranked,
                context=context,
            )

        except Exception as e:

            logger.exception(
                "Policy RAG retrieval failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    @staticmethod
    def _build_context(
        results
    ) -> str:

        sections = []

        for index, result in enumerate(
            results,
            start=1,
        ):

            sections.append(
                (
                    f"[POLICY {index}]\n"
                    f"Policy ID: "
                    f"{result.metadata.get('policy_id')}\n"
                    f"Policy Name: "
                    f"{result.metadata.get('policy_name')}\n"
                    f"Version: "
                    f"{result.metadata.get('version')}\n"
                    f"Source: "
                    f"{result.metadata.get('source')}\n"
                    f"Page: "
                    f"{result.metadata.get('page')}\n"
                    f"Score: "
                    f"{result.score:.4f}\n"
                    f"Content:\n"
                    f"{result.text}"
                )
            )
            def build_policy_filter(
    self,
    request: PolicyRequest
):

    policy_type_map = {
        "loan_eligibility": "loan",
        "apply_for_loan": "loan",
        "approve_loan": "loan",

        "initiate_refund": "refund",
        "get_refund": "refund",

        "execute_transaction": "transaction",
        "transfer_money": "transaction",
        "withdraw_money": "transaction",
    }

    policy_type = policy_type_map.get(
        request.action
    )

        if policy_type is None:
            return None

        return {
            "must": [
                {
                    "key": "policy_type",
                    "match": {
                        "value": policy_type
                    }
                }
            ]
        }

            return "\n\n".join(
                sections
            )