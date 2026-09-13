from rag.vector_store.vector_store import SimpleVectorStore


class PolicyRetriever:
    def __init__(self):
        self.vector_store = SimpleVectorStore()

    def get_relevant_policies(self, query: str, top_k: int = 3):
        results = self.vector_store.similarity_search(query, top_k=top_k)
        formatted_context = ""
        for idx, res in enumerate(results, 1):
            formatted_context += f"[{idx}] Source: {res['source']}\nContent: {res['content']}\n\n"
        return {
            "query": query,
            "results": results,
            "context": formatted_context.strip()
        }
