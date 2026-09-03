from pathlib import Path
from app.core.voice.providers.base import BaseTTSProvider
from app.core.voice.tts import ElevenLabsTTS


class ElevenLabsProvider(BaseTTSProvider):
    def __init__(self):
        self._impl = ElevenLabsTTS()

    async def synthesize(self, text: str, out_path: Path) -> Path:
        return await self._impl.synthesize(text, out_path)
