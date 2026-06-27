from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str
    QDRANT_URL: str

    OLLAMA_BASE_URL: str
    OLLAMA_MODEL: str

    OPENAI_API_KEY: str = ""
    JWT_SECRET: str
    ENVIRONMENT: str = "development"

    class Config:
        env_file = ".env"


settings = Settings()

