import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./launchmind.db"
    SECRET_KEY: str = "e8354c017d23d8c187be09c735d4f1be8d91c13d9e23fe21c210d54020de9a84"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # AI Config
    GEMINI_API_KEY: Optional[str] = None

    # Encryption Key
    ENCRYPTION_KEY: str

    # Path settings
    PROJECT_ROOT: str = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
    TMP_DIR = "/tmp"

    KNOWLEDGE_BASE_DIR: str = os.path.join(TMP_DIR, "knowledge_base")
    VECTOR_DB_DIR: str = os.path.join(TMP_DIR, "vector_db")
    UPLOADS_DIR: str = os.path.join(TMP_DIR, "uploads")

    model_config = SettingsConfigDict(
        env_file=os.path.join(PROJECT_ROOT, ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

print("===================================")
print("GEMINI_API_KEY =", settings.GEMINI_API_KEY)
print("===================================")