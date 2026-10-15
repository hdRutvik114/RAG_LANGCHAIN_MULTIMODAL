from uuid import uuid4

from pinecone import Pinecone

from app.core.config import settings


class PineconeVectorStore:

    def __init__(self):
        self.client = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.client.Index(settings.pinecone_index_name)

    def upsert_chunks(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        source: str = "unknown",
    ) -> None:

        if len(texts) != len(embeddings):
            raise ValueError("Texts and embeddings must have the same length")

        vectors = []

        for i, (text, embedding) in enumerate(zip(texts, embeddings)):
            if len(embedding) != 384:
                raise ValueError("Expected 384-dimensional embeddings")

            vectors.append({
                "id": str(uuid4()),
                "values": embedding,
                "metadata": {
                    "text": text,
                    "source": source,
                    "chunk_index": i,
                },
            })

        if vectors:
            self.index.upsert(vectors=vectors)

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> list[dict]:

        if len(query_embedding) != 384:
            raise ValueError("Expected a 384-dimensional query embedding")

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
        )

        return [
            {
                "id": match.id,
                "score": match.score,
                "text": (match.metadata or {}).get("text", ""),
                "source": (match.metadata or {}).get("source", "unknown"),
            }
            for match in results.matches
        ]
