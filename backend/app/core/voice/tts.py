from pathlib import Path
from typing import Optional
from app.config import get_settings
from app.utils.logger import logger
import asyncio

settings = get_settings()


class TTSProvider:
    async def synthesize(self, text: str, out_path: str | Path) -> Path:
        raise NotImplementedError


class Pyttsx3TTS(TTSProvider):
    """Offline fallback TTS."""

    async def synthesize(self, text: str, out_path: str | Path) -> Path:
        import pyttsx3
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        def _run():
            engine = pyttsx3.init()
            engine.save_to_file(text, str(out))
            engine.runAndWait()

        await asyncio.to_thread(_run)
        return out


class ElevenLabsTTS(TTSProvider):
    async def synthesize(self, text: str, out_path: str | Path) -> Path:
        if not settings.elevenlabs_api_key:
            raise RuntimeError("ELEVENLABS_API_KEY not set")
        try:
            from elevenlabs.client import AsyncElevenLabs
        except ImportError:
            raise RuntimeError("elevenlabs package not installed")

        client = AsyncElevenLabs(api_key=settings.elevenlabs_api_key)
        out = Path(out_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        audio = await client.generate(
            text=text,
            voice=settings.elevenlabs_voice_id,
            model="eleven_monolingual_v1",
        )
        with open(out, "wb") as f:
            async for chunk in audio:
                f.write(chunk)
        return out


def get_tts() -> TTSProvider:
    if settings.elevenlabs_api_key:
        try:
            return ElevenLabsTTS()
        except Exception:
            pass
    return Pyttsx3TTS()
