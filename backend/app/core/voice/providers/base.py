from abc import ABC, abstractmethod
from pathlib import Path


class BaseSTTProvider(ABC):
    @abstractmethod
    async def transcribe(self, audio_path: Path) -> str:
        ...


class BaseTTSProvider(ABC):
    @abstractmethod
    async def synthesize(self, text: str, out_path: Path) -> Path:
        ...
