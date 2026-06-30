from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(
    title="Enterprise RAG Platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG Platform API"
    }

from app.api.v1.chat import (
    router as chat_router,
)

app.include_router(
    chat_router,
    prefix="/api/v1/chat",
    tags=["Chat"],
)

app.include_router(api_router)


from app.api.v1.conversations import (
    router as conversation_router,
)

app.include_router(
    conversation_router,
    prefix="/api/v1/conversations",
    tags=["Conversations"],
)