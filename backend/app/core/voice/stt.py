from typing import Optional
from pathlib import Path
from app.utils.logger import logger
from app.config import get_settings

settings = get_settings()


class STTProvider:
    async def transcribe(self, audio_path: str | Path) -> str:
        raise NotImplementedError


class WhisperSTT(STTProvider):
    def __init__(self, model_name: str = "base"):
        self.model_name = model_name
        self._model = None

    def _load(self):
        if self._model is None:
            try:
                import whisper
                self._model = whisper.load_model(self.model_name)
                logger.info(f"Whisper model '{self.model_name}' loaded")
            except ImportError:
                logger.warning("openai-whisper not installed")
                raise

    async def transcribe(self, audio_path: str | Path) -> str:
        self._load()
        import asyncio
        result = await asyncio.to_thread(self._model.transcribe, str(audio_path))
        return result.get("text", "").strip()


def get_stt() -> STTProvider:
    return WhisperSTT(settings.whisper_model)
