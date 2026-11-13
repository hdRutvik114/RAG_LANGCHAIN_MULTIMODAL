from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore
from app.services.ingestionservice import IngestionService


def main():
    embedding_service = TextEmbeddingService()
    vector_store = PineconeVectorStore()

    ingestion_service = IngestionService(
        embedding_service=embedding_service,
        vector_store=vector_store,
    )

    result = ingestion_service.ingest_file(
        "C:/Users/YATIRAJ/OneDrive/Desktop/MULTIMODAL_RAG/multimodal-rag-api/data/documents/attention.pdf"
    )

    print("\nIngestion Result:")
    print(result)


if __name__ == "__main__":
    main()