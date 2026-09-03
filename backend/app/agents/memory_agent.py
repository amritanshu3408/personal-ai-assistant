from typing import Any, Dict, Optional, AsyncGenerator
from app.agents.base import BaseAgent
from app.agents.conversation import ConversationAgent


class MemoryAgent(BaseAgent):
    name = "memory_agent"
    description = "Specialized for memory store/recall"

    def __init__(self):
        self._conv = ConversationAgent()

    async def handle(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        async for event in self._conv.handle(message, context):
            yield event
