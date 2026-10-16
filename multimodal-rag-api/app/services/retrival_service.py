
from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore


class RetrievalService:

    def __init__(self):
        self.embedding_service = TextEmbeddingService()
        self.vector_store = PineconeVectorStore()

    def retrieve(self, query: str, top_k: int = 5) -> list[dict]:
        if not query.strip():
            raise ValueError("Query cannot be empty")

        query_embedding = self.embedding_service.embed_query(query)

        results = self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
        )

        return results
