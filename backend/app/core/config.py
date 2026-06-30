from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    QDRANT_URL: str

    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str

    OPENAI_API_KEY: str = ""

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()