import sys

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from ml.utils.exception import MyException
from ml.utils.logger import logger


class QdrantVectorStore:

    def __init__(
        self,
        url: str = "http://localhost:6333",
        collection_name: str = "bank_policies",
        vector_size: int = 384,
    ):

        try:

            self.collection_name = (
                collection_name
            )

            self.client = QdrantClient(
                url=url
            )

            self._create_collection(
                vector_size
            )

            logger.info(
                f"Qdrant initialized: "
                f"collection="
                f"{collection_name}"
            )

        except Exception as e:

            logger.exception(
                "Qdrant initialization failed"
            )

            raise MyException(
                e,
                sys
            ) from e

    def _create_collection(
        self,
        vector_size: int
    ):

        collections = (
            self.client
            .get_collections()
            .collections
        )

        names = {
            collection.name
            for collection in collections
        }

        if self.collection_name not in names:

            self.client.create_collection(
                collection_name=(
                    self.collection_name
                ),
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

            logger.info(
                f"Created Qdrant collection: "
                f"{self.collection_name}"
            )

    def upsert(
        self,
        chunks,
        embeddings
    ):

        points = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            payload = {
                "text": chunk.text,
                "chunk_id": chunk.chunk_id,
                **chunk.metadata,
            }

            points.append(
                PointStruct(
                    id=chunk.chunk_id,
                    vector=embedding.tolist(),
                    payload=payload
                )
            )

        self.client.upsert(
            collection_name=(
                self.collection_name
            ),
            points=points
        )

        logger.info(
            f"Upserted {len(points)} "
            f"chunks into Qdrant"
        )

    def search(
        self,
        query_vector,
        top_k: int = 10,
        query_filter=None
    ):

        results = self.client.query_points(
            collection_name=(
                self.collection_name
            ),
            query=query_vector.tolist(),
            query_filter=query_filter,
            with_payload=True,
            limit=top_k
        ).points

        return results