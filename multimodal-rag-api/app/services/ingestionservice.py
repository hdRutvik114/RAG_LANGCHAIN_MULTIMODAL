
import hashlib
from pathlib import Path

from langchain_core.documents import Document

from app.core.database import SessionLocal
from app.embeddings.text_embeddings import TextEmbeddingService
from app.ingestion.chunker import split_document
from app.ingestion.loader import load_text_file
from app.models.document import Document as DocumentRecord
from app.repositories.document_repository import DocumentRepository
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

        # Read the existing registry record and mark ingestion as processing.
        with SessionLocal() as session:
            repository = DocumentRepository(session)
            record = repository.get_by_document_id(document_id)

            if (
                record is not None
                and record.current_content_hash == content_hash
                and record.status == "completed"
            ):
                return {
                    "filename": source,
                    "document_id": document_id,
                    "content_hash": content_hash,
                    "chunks_created": record.chunk_count,
                    "chunks_stored": 0,
                    "status": "skipped",
                    "message": "Document content is unchanged.",
                }

            previous_hash = (
                record.current_content_hash if record is not None else None
            )

            if record is None:
                record = DocumentRecord(
                    document_id=document_id,
                    source=source,
                    status="processing",
                    chunk_count=0,
                )
                repository.create(record)
            else:
                record.source = source
                record.status = "processing"
                record.error_message = None
                repository.save(record)

            # Persist processing state before calling Pinecone.
            session.commit()

        try:
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

            if len(texts) != len(embeddings):
                raise ValueError(
                    "Embedding count does not match chunk count"
                )

            # Deterministic IDs make retries of this version repeatable.
            vector_ids = self.vector_store.upsert_chunks(
                texts=texts,
                embeddings=embeddings,
                document_id=document_id,
                content_hash=content_hash,
                source=source,
            )

            if len(vector_ids) != len(texts):
                raise RuntimeError(
                    "Not all document chunks were stored"
                )

            # Remove the previous version only after the new upsert succeeds.
            if previous_hash and previous_hash != content_hash:
                self.vector_store.delete_document_version(
                    document_id=document_id,
                    content_hash=previous_hash,
                )

            # Mark this version current only after vector operations succeed.
            with SessionLocal() as session:
                repository = DocumentRepository(session)
                record = repository.get_by_document_id(document_id)

                if record is None:
                    raise RuntimeError(
                        "Document registry record disappeared"
                    )

                record.current_content_hash = content_hash
                record.status = "completed"
                record.chunk_count = len(vector_ids)
                record.error_message = None
                repository.save(record)
                session.commit()

            return {
                "filename": source,
                "document_id": document_id,
                "content_hash": content_hash,
                "chunks_created": len(chunks),
                "chunks_stored": len(vector_ids),
                "status": "completed",
            }

        except Exception as exc:
            # Preserve the previous hash so a failed update can be retried.
            try:
                with SessionLocal() as session:
                    repository = DocumentRepository(session)
                    record = repository.get_by_document_id(document_id)

                    if record is not None:
                        record.status = "failed"
                        record.error_message = str(exc)[:2000]
                        repository.save(record)
                        session.commit()
            except Exception:
                # Preserve the original ingestion error if status recording fails.
                pass

            raise
