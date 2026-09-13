from rag.chunking.splitter import (
    PolicyChunker,
)

from rag.embeddings.embedding_model import (
    EmbeddingModel,
)

from rag.ingestion.loader import (
    PDFLoader,
)

from rag.ingestion.cleaner import (
    DocumentCleaner,
)

from rag.retrieval.qdrant import (
    QdrantVectorStore,
)

from rag.retrieval.retriever import (
    PolicyRetriever,
)

from rag.retrieval.reranker import (
    PolicyReranker,
)


class PolicyRAGPipeline:

    def __init__(self):

        self.loader = PDFLoader()

        self.cleaner = (
            DocumentCleaner()
        )

        self.chunker = PolicyChunker(
            chunk_size=800,
            chunk_overlap=120
        )

        self.embedding_model = (
            EmbeddingModel()
        )

        self.vector_store = (
            QdrantVectorStore(
                url="http://localhost:6333",
                collection_name=(
                    "bank_policies"
                ),
                vector_size=384
            )
        )

        self.retriever = (
            PolicyRetriever(
                embedding_model=(
                    self.embedding_model
                ),
                vector_store=(
                    self.vector_store
                )
            )
        )

        self.reranker = (
            PolicyReranker()
        )

    def ingest(
        self,
        file_path: str,
        metadata: dict
    ):

        documents = self.loader.load(
            file_path
        )

        for document in documents:

            document["text"] = (
                self.cleaner.clean(
                    document["text"]
                )
            )

            document["metadata"].update(
                metadata
            )

        chunks = self.chunker.split(
            documents
        )

        embeddings = (
            self.embedding_model.encode(
                [
                    chunk.text
                    for chunk in chunks
                ]
            )
        )

        self.vector_store.upsert(
            chunks=chunks,
            embeddings=embeddings
        )

        return chunks

    def retrieve(
        self,
        query: str,
        top_k: int = 5
    ):

        candidates = (
            self.retriever.retrieve(
                query=query,
                top_k=10
            )
        )

        return self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k
        )