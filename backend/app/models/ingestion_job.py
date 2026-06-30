from datetime import datetime
from enum import Enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
)

from app.db.session import Base


class IngestionJobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class IngestionJob(Base):
    __tablename__ = "ingestion_jobs"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    tenant_id = Column(
        Integer,
        ForeignKey("tenants.id"),
        nullable=False,
        index=True,
    )

    document_id = Column(
        Integer,
        ForeignKey(
            "documents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    status = Column(
        String,
        nullable=False,
        default=IngestionJobStatus.PENDING.value,
    )

    error_message = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    started_at = Column(
        DateTime,
        nullable=True,
    )

    completed_at = Column(
        DateTime,
        nullable=True,
    )