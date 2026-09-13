from dataclasses import dataclass, field
from typing import Any


@dataclass
class DocumentChunk:

    chunk_id: str

    text: str

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class RetrievedChunk:

    chunk_id: str

    text: str

    score: float

    metadata: dict[str, Any] = field(
        default_factory=dict
    )


@dataclass
class RAGResult:

    query: str

    results: list[RetrievedChunk]

    context: str