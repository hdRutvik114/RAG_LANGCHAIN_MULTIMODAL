from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from app.models.document import DocumentChunk


class DocumentChunkRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_many(
        self,
        chunks: list[DocumentChunk],
    ) -> None:
        self.session.add_all(chunks)
        self.session.flush()

    def get_by_document_version(
        self,
        document_id: str,
        content_hash: str,
    ) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .where(
                DocumentChunk.document_id == document_id,
                DocumentChunk.content_hash == content_hash,
            )
            .order_by(DocumentChunk.chunk_index)
        )
        return list(self.session.scalars(statement).all())

    def delete_document_version(
        self,
        document_id: str,
        content_hash: str,
    ) -> None:
        statement = delete(DocumentChunk).where(
            DocumentChunk.document_id == document_id,
            DocumentChunk.content_hash == content_hash,
        )
        self.session.execute(statement)