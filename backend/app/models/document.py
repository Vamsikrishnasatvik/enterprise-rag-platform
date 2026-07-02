from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    JSON,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from app.db.session import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    file_type = Column(
        String,
        nullable=False,
    )

    file_size = Column(
        Integer,
        nullable=False,
    )

    storage_path = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        nullable=False,
        default="UPLOADED",
    )

    # ==========================
    # Metadata fields
    # ==========================

    department = Column(
        String,
        nullable=True,
    )

    category = Column(
        String,
        nullable=True,
    )

    source = Column(
        String,
        nullable=True,
    )

    tags = Column(
        JSON,
        nullable=True,
    )

    # ==========================

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
    )

    ingestion_jobs = relationship(
        "IngestionJob",
        backref="document",
        cascade="all, delete-orphan",
    )