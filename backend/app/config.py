import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "JARVIS-X"
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "llama3")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/jarvisx")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "SUPER_SECRET_COMPROMISED_KEY_CHANGE_THIS")
    ALGORITHM: str = "HS256"

settings = Settings()