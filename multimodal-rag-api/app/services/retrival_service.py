
from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore


class RetrievalService:
    def __init__(
        self,
        embedding_service: TextEmbeddingService,
        vector_store: PineconeVectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")

        query_embedding = self.embedding_service.embed_query(query)

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )
