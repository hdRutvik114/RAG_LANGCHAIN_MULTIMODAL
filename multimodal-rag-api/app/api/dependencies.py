from functools import lru_cache

from app.core.config import Settings, settings
from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore
from app.llm.model_provider import get_chat_model

from app.services.retrival_service import RetrievalService
from app.services.generation_service import GenerationService
from app.services.rag_service import RAGService
from app.reranking.cross_encoder import CrossEncoderReranker
from app.retrival.bm25_retriver import BM25Retriever

def get_settings() -> Settings:
    return settings

@lru_cache(maxsize=1)
def get_bm25_retriever() -> BM25Retriever:
    return BM25Retriever()

@lru_cache(maxsize=1)
def get_embedding_service() -> TextEmbeddingService:
    return TextEmbeddingService()

@lru_cache(maxsize=1)
def get_reranker() -> CrossEncoderReranker:
    return CrossEncoderReranker()

@lru_cache(maxsize=1)
def get_vector_store() -> PineconeVectorStore:
    return PineconeVectorStore()


def get_retrieval_service() -> RetrievalService:
    return RetrievalService(
        embedding_service=get_embedding_service(),
        vector_store=get_vector_store(),
        reranker=get_reranker(),
        bm25_retriever=get_bm25_retriever(),
    )


def get_generation_service() -> GenerationService:
    return GenerationService(
        chat_model=get_chat_model(),
    )


def get_rag_service() -> RAGService:
    return RAGService(
        retrieval_service=get_retrieval_service(),
        generation_service=get_generation_service(),
        bm25_retriever=get_bm25_retriever(),
    )
