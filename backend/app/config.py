from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # LLM
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str | None = None

    # Voice
    whisper_model: str = "base"
    elevenlabs_api_key: str = ""
    elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM"

    # Server
    host: str = "127.0.0.1"
    port: int = 8000
    debug: bool = True
    allowed_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Memory
    memory_db_path: str = "./data/memory.db"
    embedding_model: str = "text-embedding-3-small"

    @property
    def origins_list(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def data_dir(self) -> Path:
        p = Path(self.memory_db_path).parent
        p.mkdir(parents=True, exist_ok=True)
        return p


@lru_cache
def get_settings() -> Settings:
    return Settings()
