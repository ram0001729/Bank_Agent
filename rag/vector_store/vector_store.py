import math
from typing import List, Dict, Any


def simple_hash_embedding(text: str, dim: int = 64) -> List[float]:
    """Dense vector embedding generator for text."""
    vec = [0.0] * dim
    words = text.lower().split()
    for word in words:
        for idx, char in enumerate(word):
            vec[(ord(char) * (idx + 1)) % dim] += 1.0
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return [v / norm for v in vec]


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1)) or 1.0
    norm2 = math.sqrt(sum(b * b for b in vec2)) or 1.0
    return dot / (norm1 * norm2)


class SimpleVectorStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SimpleVectorStore, cls).__new__(cls)
            cls._instance.documents = []
        return cls._instance

    def add_documents(self, docs: List[Dict[str, Any]]):
        """Docs: list of dicts with 'content', 'source', 'metadata'."""
        for doc in docs:
            embedding = simple_hash_embedding(doc["content"])
            doc_entry = {
                "content": doc["content"],
                "source": doc.get("source", "unknown"),
                "metadata": doc.get("metadata", {}),
                "embedding": embedding
            }
            self.documents.append(doc_entry)

    def similarity_search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_vec = simple_hash_embedding(query)
        scored = []
        for doc in self.documents:
            score = cosine_similarity(query_vec, doc["embedding"])
            scored.append({
                "content": doc["content"],
                "source": doc["source"],
                "score": score
            })
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
