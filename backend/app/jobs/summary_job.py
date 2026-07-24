from app.db.session import SessionLocal
from app.agents.summarizer_agent import SummarizerAgent


def summarize_conversation(
    conversation_id: int,
):
    db = SessionLocal()

    try:
        SummarizerAgent().run(
            db=db,
            conversation_id=conversation_id,
        )
    finally:
        db.close()