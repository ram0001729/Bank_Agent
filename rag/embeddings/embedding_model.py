import sys

from sentence_transformers import SentenceTransformer

from ml.utils.exception import MyException
from ml.utils.logger import logger


class EmbeddingModel:

    def __init__(
        self,
        model_name: str = (
            "sentence-transformers/"
            "all-MiniLM-L6-v2"
        )
    ):

        try:

            self.model_name = model_name

            self.model = (
                SentenceTransformer(
                    model_name
                )
            )

            logger.info(
                f"Embedding model loaded: "
                f"{model_name}"
            )

        except Exception as e:

            logger.exception(
                "Failed to load embedding model"
            )

            raise MyException(
                e,
                sys
            ) from e

    def encode(
        self,
        texts: list[str]
    ):

        return self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=False
        )

    def encode_query(
        self,
        query: str
    ):

        return self.model.encode(
            query,
            normalize_embeddings=True
        )