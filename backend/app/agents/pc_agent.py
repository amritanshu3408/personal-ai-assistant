from typing import Any, Dict, Optional, AsyncGenerator
from app.agents.base import BaseAgent
from app.agents.conversation import ConversationAgent


class PCAgent(BaseAgent):
    name = "pc_agent"
    description = "Specialized for PC control tasks"

    def __init__(self):
        self._conv = ConversationAgent()

    async def handle(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        # Re-use conversation agent; in future can restrict tools
        async for event in self._conv.handle(message, context):
            yield event
