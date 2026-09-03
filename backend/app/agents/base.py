from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, AsyncGenerator


class BaseAgent(ABC):
    name: str
    description: str

    @abstractmethod
    async def handle(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        ...
