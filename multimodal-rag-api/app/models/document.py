from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import (
    DateTime, String, Text, func,
    ForeignKey, UniqueConstraint,
)
from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    document_id: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )

    source: Mapped[str] = mapped_column(String(255), nullable=False)

    current_content_hash: Mapped[str | None] = mapped_column(
        String(64), nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )

    chunk_count: Mapped[int] = mapped_column(nullable=False, default=0)

    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    
    
class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    __table_args__ = (
        UniqueConstraint(
            "document_id",
            "content_hash",
            "chunk_index",
            name="uq_document_chunk_version_index",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    vector_id: Mapped[str] = mapped_column(
        String(64), unique=True, index=True, nullable=False
    )

    document_id: Mapped[str] = mapped_column(
        String(64),
        ForeignKey("documents.document_id"),
        index=True,
        nullable=False,
    )

    content_hash: Mapped[str] = mapped_column(
        String(64), nullable=False
    )

    chunk_index: Mapped[int] = mapped_column(nullable=False)

    text: Mapped[str] = mapped_column(Text, nullable=False)

    page: Mapped[int | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )