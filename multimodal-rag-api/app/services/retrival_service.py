from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore
from app.reranking.cross_encoder import CrossEncoderReranker
from app.retrival.bm25_retriver import BM25Retriever
from app.retrival.rank_fusion import  reciprocal_rank_fusion

class RetrievalService:
    def __init__(
        self,
        embedding_service: TextEmbeddingService,
        vector_store: PineconeVectorStore,
        reranker: CrossEncoderReranker ,         
        bm25_retriever: BM25Retriever,
        ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.reranker = reranker
        self.bm25_retriever = bm25_retriever
        
        

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
        # print("documents which will be sent for reranking:", candidates)

        return self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k,
        )
        
    def retrieve_hybrid(self,query: str,top_k: int = 5,candidate_k: int = 20,document_id: str | None = None,
    ) -> list[dict]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty")
    
        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")
    
        if not top_k <= candidate_k <= 50:
            raise ValueError("candidate_k must be between top_k and 50")
    
        if self.bm25_retriever is None:
            raise RuntimeError("BM25 retriever is not configured")
    
        # Semantic retrieval from Pinecone
        dense_results = self.retrieve(
            query=query,
            top_k=candidate_k,
            document_id=document_id,
        )
    
        # Keyword retrieval from PostgreSQL
        bm25_results = self.bm25_retriever.search(
            query=query,
            top_k=candidate_k,
            document_id=document_id,
        )
    
        # Combine both rankings
        return reciprocal_rank_fusion(
            ranked_lists=[dense_results, bm25_results],
            top_k=top_k,
        )
    def retrieve_hybrid_reranked(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 20,
        document_id: str | None = None,
    ) -> list[dict]:

        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        if self.reranker is None:
            raise RuntimeError("Reranker has not been configured")

        if not 1 <= top_k <= 50:
            raise ValueError("top_k must be between 1 and 50")

        if not top_k <= candidate_k <= 50:
            raise ValueError("candidate_k must be between top_k and 50")

        # Step 1: Retrieve and fuse the top candidate_k results.
        candidates = self.retrieve_hybrid(
            query=query,
            top_k=candidate_k,
            candidate_k=candidate_k,
            document_id=document_id,
        )

        # Step 2: Rerank fused candidates using the cross-encoder.
        return self.reranker.rerank(
            query=query,
            documents=candidates,
            top_k=top_k,
        )