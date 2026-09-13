import os
import re
from rag.chunking.splitter import RecursiveTextSplitter
from rag.vector_store.vector_store import SimpleVectorStore


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text lines from PDF file."""
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read().decode('latin1', errors='ignore')
        # Extract text inside parenthesis (Tj operator in PDF)
        matches = re.findall(r'\((.*?)\)\s*Tj', content)
        if matches:
            return "\n".join(matches)
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return ""


def ingest_policy_documents():
    docs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "documents")
    splitter = RecursiveTextSplitter(chunk_size=250, chunk_overlap=30)
    vector_store = SimpleVectorStore()

    documents_to_add = []
    pdf_count = 0

    for root, _, files in os.walk(docs_dir):
        for f in files:
            if f.endswith('.pdf'):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, docs_dir)
                raw_text = extract_text_from_pdf(full_path)

                if raw_text:
                    chunks = splitter.split_text(raw_text)
                    for chunk in chunks:
                        documents_to_add.append({
                            "content": chunk,
                            "source": rel_path,
                            "metadata": {"filename": f}
                        })
                    pdf_count += 1

    vector_store.add_documents(documents_to_add)
    print(f"RAG Ingestion Complete: Processed {pdf_count} PDF policies into {len(documents_to_add)} vector chunks.")
    return len(documents_to_add)


if __name__ == "__main__":
    ingest_policy_documents()
