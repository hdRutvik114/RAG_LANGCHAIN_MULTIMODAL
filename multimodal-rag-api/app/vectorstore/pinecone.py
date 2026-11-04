
from hashlib import sha256

from pinecone import Pinecone

from app.core.config import settings


class PineconeVectorStore:
    def __init__(self):
        self.client = Pinecone(api_key=settings.pinecone_api_key)
        self.index = self.client.Index(settings.pinecone_index_name)

    @staticmethod
    def create_chunk_id(
        document_id: str,
        content_hash: str,
        chunk_index: int,
    ) -> str:
        identity = f"{document_id}:{content_hash}:{chunk_index}"
        return sha256(identity.encode("utf-8")).hexdigest()

    def upsert_chunks(
        self,
        texts: list[str],
        embeddings: list[list[float]],
        document_id: str,
        content_hash: str,
        source: str,
        chunk_metadata: list[dict] | None = None
    ) -> list[str]:
        if chunk_metadata is None:
            chunk_metadata = [{} for _ in texts]
        
        if len(texts) != len(embeddings):
            raise ValueError("Texts and embeddings must have the same length")

        vector_ids = []

        for chunk_index, embedding in enumerate(embeddings):
            if len(embedding) != 384:
                raise ValueError("Expected 384-dimensional embeddings")

            vector_ids.append(
                self.create_chunk_id(
                    document_id=document_id,
                    content_hash=content_hash,
                    chunk_index=chunk_index,
                )
            )

        vectors = [
            {
                "id": vector_id,
                "values": embedding,
                "metadata": {
                    "text": text,
                    "source": source,
                    "document_id": document_id,
                    "content_hash": content_hash,
                    "chunk_index": chunk_index,
                    **chunk_metadata[chunk_index],
                },
            }
            for chunk_index, (text, embedding, vector_id) in enumerate(
                zip(texts, embeddings, vector_ids)
            )
        ]

        if vectors:
            self.index.upsert(vectors=vectors)

        return vector_ids

    def delete_document_version(
        self,
        document_id: str,
        content_hash: str,
    ) -> None:
        self.index.delete(
            filter={
                "document_id": {"$eq": document_id},
                "content_hash": {"$eq": content_hash},
            }
        )

    def search(
        self,
        query_embedding: list[float],
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[dict]:
        if len(query_embedding) != 384:
            raise ValueError("Expected 384-dimensional query embeddings")

        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")
    #this is the code that was added to the retrival_service.py file to allow for filtering by document_id in the search method of the PineconeVectorStore class.
    # which is used in the retrieve method of the RetrievalService class. The filter_conditions dictionary is created to hold the filter conditions for the search query. If a document_id is provided, it adds a filter condition to only return results that match the specified document_id. The search method then uses this filter_conditions dictionary when querying the Pinecone index.
        filter_conditions = {}
        if document_id is not None:
            filter_conditions["document_id"] = {"$eq": document_id}

        
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True,
            filter=filter_conditions,
        )

        return [
            {
                "id": match.id,
                "score": match.score,
                "text": (match.metadata or {}).get("text", ""),
                "source": (match.metadata or {}).get("source", "unknown"),
                "page": (match.metadata or {}).get("page"),
                "document_id": (match.metadata or {}).get("document_id", ""),
                "content_hash": (match.metadata or {}).get("content_hash", ""),
                "chunk_index": (match.metadata or {}).get("chunk_index", -1),
                "chunk_index": (match.metadata or {}).get("chunk_index", -1),
                
            }
            for match in results.matches
        ]
