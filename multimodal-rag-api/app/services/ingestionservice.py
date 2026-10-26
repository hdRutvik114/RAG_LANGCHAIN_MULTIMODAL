
import hashlib
from pathlib import Path

from langchain_core.documents import Document

from app.ingestion.loader import load_text_file
from app.ingestion.chunker import split_document
from app.embeddings.text_embeddings import TextEmbeddingService
from app.vectorstore.pinecone import PineconeVectorStore


class IngestionService:
    def __init__(
        self,
        embedding_service: TextEmbeddingService,
        vector_store: PineconeVectorStore,
    ):
        self.embedding_service = embedding_service
        self.vector_store = vector_store
    @staticmethod
    def _create_document_id(file_path: str) -> str:
        normalized_path = str(Path(file_path).resolve()).lower()
        return hashlib.sha256(
            normalized_path.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def _create_content_hash(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def ingest_file(self, file_path: str) -> dict:
        path = Path(file_path).resolve()
        text = load_text_file(str(path))

        if not text.strip():
            raise ValueError("File contains no text")

        document_id = self._create_document_id(str(path))
        content_hash = self._create_content_hash(text)
        source = path.name

        document = Document(
            page_content=text,
            metadata={
                "source": source,
                "document_id": document_id,
                "content_hash": content_hash,
            },
        )

        chunks = split_document(document)

        if not chunks:
            raise ValueError("Document produced no chunks")

        texts = [chunk.page_content for chunk in chunks]
        embeddings = self.embedding_service.embed_documents(texts)

        vector_ids = self.vector_store.upsert_chunks(
            texts=texts,
            embeddings=embeddings,
            document_id=document_id,
            content_hash=content_hash,
            source=source,
        )

        return {
            "filename": source,
            "document_id": document_id,
            "content_hash": content_hash,
            "chunks_created": len(chunks),
            "chunks_stored": len(vector_ids),
        }
