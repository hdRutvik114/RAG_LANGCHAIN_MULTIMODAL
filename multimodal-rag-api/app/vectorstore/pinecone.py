from langchain_pinecone import PineconeVectorStore

from app.core.config import settings
from app.embeddings.text_embeddings import TextEmbeddingService


class PineconeStore:

    def __init__(self):
        self.embedding_service = TextEmbeddingService()

        self.vector_store = PineconeVectorStore(
            index_name="multimodal-rag",
            embedding=self.embedding_service.model,
            pinecone_api_key=settings.pinecone_api_key,
        )