from app.db.session import Base

# Import all models here for Alembic
from app.models.document import Document
from app.models.document_chunk import DocumentChunk
from app.models.conversation import Conversation
from app.models.message import Message