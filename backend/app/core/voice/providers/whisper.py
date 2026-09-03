from pathlib import Path
from app.core.voice.providers.base import BaseSTTProvider
from app.core.voice.stt import WhisperSTT


class WhisperProvider(BaseSTTProvider):
    def __init__(self, model: str = "base"):
        self._impl = WhisperSTT(model)

    async def transcribe(self, audio_path: Path) -> str:
        return await self._impl.transcribe(audio_path)
