import sys

from sentence_transformers import CrossEncoder

from rag.schemas import RetrievedChunk

from ml.utils.exception import MyException
from ml.utils.logger import logger


class PolicyReranker:

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/"
            "ms-marco-MiniLM-L6-v2"
        )
    ):

        try:

            self.model = CrossEncoder(
                model_name
            )

            logger.info(
                f"Reranker loaded: "
                f"{model_name}"
            )

        except Exception as e:

            logger.exception(
                "Failed to load reranker"
            )

            raise MyException(
                e,
                sys
            ) from e

    def rerank(
        self,
        query: str,
        documents: list[RetrievedChunk],
        top_k: int = 5
    ) -> list[RetrievedChunk]:

        if not documents:

            return []

        pairs = [
            [
                query,
                document.text
            ]
            for document in documents
        ]

        scores = self.model.predict(
            pairs,
            batch_size=16,
            show_progress_bar=False
        )

        ranked = []

        for document, score in zip(
            documents,
            scores
        ):

            document.score = float(
                score
            )

            ranked.append(
                document
            )

        ranked.sort(
            key=lambda x: x.score,
            reverse=True
        )

        return ranked[:top_k]