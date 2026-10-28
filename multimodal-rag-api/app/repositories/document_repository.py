from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.document import Document


class DocumentRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_by_document_id(self, document_id: str) -> Document | None:
        statement = select(Document).where(
            Document.document_id == document_id
        )
        return self.session.scalar(statement)

    def create(self, document: Document) -> Document:
        self.session.add(document)
        self.session.flush()
        return document

    def save(self, document: Document) -> Document:
        self.session.add(document)
        self.session.flush()
        return document