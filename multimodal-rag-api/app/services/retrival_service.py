from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore
from app.reranking.cross_encoder import CrossEncoderReranker


class RetrievalService:
    def __init__(
        self,
        embedding_service: TextEmbeddingService,
        vector_store: PineconeVectorStore,
        reranker: CrossEncoderReranker | None = None,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.reranker = reranker

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        document_id: str | None = None,
    ) -> list[dict]:

        if not query.strip():
            raise ValueError("Query cannot be empty")

        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")

        query_embedding = self.embedding_service.embed_query(query)

        return self.vector_store.search(
            query_embedding=query_embedding,
            top_k=top_k,
            document_id=document_id,
        )

    def retrieve_reranked(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 10,
        document_id: str | None = None,
    ) -> list[dict]:

        if self.reranker is None:
            raise RuntimeError("Reranker has not been configured")

        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")

        if not top_k <= candidate_k <= 50:
            raise ValueError("candidate_k must be between top_k and 50")

        candidates = self.retrieve(
            query=query,
            top_k=candidate_k,
            document_id=document_id,
        )

        return self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k,
        )