from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/story_ai"

    # Telnyx
    TELNYX_API_KEY: str = ""
    TELNYX_PUBLIC_KEY: str = ""
    TELNYX_PHONE_NUMBER: str = ""

    # OpenAI or other AI service
    OPENAI_API_KEY: str = ""

    # Comet ML
    COMET_API_KEY: str = ""
    COMET_PROJECT_NAME: str = "story-ai"
    COMET_WORKSPACE: str = ""

    # MemVerge (if configuration needed)
    MEMVERGE_CONFIG: Optional[str] = None

    # App settings
    APP_NAME: str = "Story AI"
    DEBUG: bool = True
    API_VERSION: str = "v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
