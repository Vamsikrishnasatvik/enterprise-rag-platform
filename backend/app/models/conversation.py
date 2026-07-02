from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Text,
    JSON,
)

from sqlalchemy.orm import relationship

from app.db.session import Base


class Conversation(Base):
    __tablename__ = "conversations"

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

    title = Column(
        String,
        nullable=True,
    )

    summary = Column(
        Text,
        nullable=True,
    )

    message_count = Column(
        Integer,
        nullable=False,
        default=0,
    )

    last_message_at = Column(
        DateTime,
        nullable=True,
    )

    conversation_metadata = Column(
        JSON,
        nullable=True,
        default=dict,
    )

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

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    summaries = relationship(
        "ConversationSummary",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )