from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.loader import load_text_file
from app.ingestion.chunker import split_document
from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore


class IngestionService:

    def __init__(self):
        self.embedding_service = TextEmbeddingService()
        self.vector_store = PineconeVectorStore()

    def ingest_file(self, file_path: str) -> dict:
        text = load_text_file(file_path)

        if not text.strip():
            raise ValueError("File contains no text")

        document = Document(
            page_content=text,
            metadata={"source": Path(file_path).name},
        )

        chunks = split_document(document)
        texts = [chunk.page_content for chunk in chunks]

        embeddings = self.embedding_service.embed_documents(texts)

        self.vector_store.upsert_chunks(
            texts=texts,
            embeddings=embeddings,
            source=Path(file_path).name,
        )

        return {
            "filename": Path(file_path).name,
            "chunks_created": len(chunks),
            "chunks_stored": len(embeddings),
        }