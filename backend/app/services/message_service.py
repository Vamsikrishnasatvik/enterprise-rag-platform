from sqlalchemy.orm import Session

from app.models.message import Message

def create_message(
    db: Session,
    conversation_id: int,
    tenant_id: int,
    role: str,
    content: str,
):

    print("=" * 60)
    print("CREATE MESSAGE")
    print("conversation_id:", conversation_id)
    print("tenant_id:", tenant_id)
    print("role:", role)
    print("=" * 60)
    
    message = Message(
        conversation_id=conversation_id,
        tenant_id=tenant_id,
        role=role,
        content=content,
    )

    db.add(message)
    db.commit()
    db.refresh(message)


    return message


def get_messages(
    db: Session,
    conversation_id: int,
):
    return (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )


def _format_messages(messages: list[Message]) -> list[dict]:
    """
    Convert Message ORM objects into chat history format.
    """
    return [
        {
            "role": message.role,
            "content": message.content,
        }
        for message in messages
    ]


def get_chat_history(
    db: Session,
    conversation_id: int,
):
    messages = get_messages(
        db=db,
        conversation_id=conversation_id,
    )

    return _format_messages(messages)


def get_recent_messages(
    db: Session,
    conversation_id: int,
    limit: int = 10,
):
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc())
        .limit(limit)
        .all()
    )

    # Reverse so the oldest of the recent messages comes first
    messages.reverse()

    return _format_messages(messages)