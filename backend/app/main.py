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


app.include_router(api_router)