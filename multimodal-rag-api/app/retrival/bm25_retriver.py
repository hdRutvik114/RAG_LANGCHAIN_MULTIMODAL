import re
from threading import RLock

from rank_bm25 import BM25Okapi

from app.core.database import SessionLocal
from app.repositories.document_chunk_repository import (
    DocumentChunkRepository,
)


class BM25Retriever:

    def __init__(self):
        # Cache BM25 indexes so we don't rebuild them for every query.
        self._cache: dict[str | None, dict] = {}
        self._lock = RLock()

    @staticmethod
    def _tokenize(text: str) -> list[str]:
        return re.findall(r"\b\w+\b", text.lower())

    def _build_index(self, document_id: str | None = None) -> dict | None:

        with SessionLocal() as session:
            repository = DocumentChunkRepository(session)
            rows = repository.get_current_chunks(document_id)

            if not rows:
                return None

            chunks = [row[0] for row in rows]
            sources = [row[1] for row in rows]

            corpus = [
                self._tokenize(chunk.text)
                for chunk in chunks
            ]

            if not any(corpus):
                return None

            return {
                "bm25": BM25Okapi(corpus),
                "chunks": chunks,
                "sources": sources,
            }

    def _get_index(self, document_id: str | None = None) -> dict | None:

        with self._lock:
            if document_id not in self._cache:
                self._cache[document_id] = self._build_index(document_id)

            return self._cache[document_id]

    def refresh(self, document_id: str | None = None) -> None:
        """
        Rebuild the cached index.

        document_id=None refreshes the index containing all documents.
        A specific document_id refreshes only that document's index.
        """
        with self._lock:
            self._cache[document_id] = self._build_index(document_id)

    def search(
        self,
        query: str,
        top_k: int = 10,
        document_id: str | None = None,
    ) -> list[dict]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")

        query_tokens = self._tokenize(query)

        if not query_tokens:
            return []

        index = self._get_index(document_id)

        if index is None:
            return []

        scores = index["bm25"].get_scores(query_tokens)
        chunks = index["chunks"]
        sources = index["sources"]

        ranked_indices = sorted(
            range(len(scores)),
            key=lambda i: scores[i],
            reverse=True,
        )

        results = []

        for i in ranked_indices[:top_k]:
            chunk = chunks[i]

            results.append({
                "id": chunk.vector_id,
                "score": float(scores[i]),
                "text": chunk.text,
                "source": sources[i],
                "page": chunk.page,
                "document_id": chunk.document_id,
                "content_hash": chunk.content_hash,
                "chunk_index": chunk.chunk_index,
            })

        return results