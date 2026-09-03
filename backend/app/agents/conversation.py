from typing import Any, Dict, Optional, AsyncGenerator, List
from app.agents.base import BaseAgent
from app.core.orchestrator import Orchestrator


class ConversationAgent(BaseAgent):
    name = "conversation"
    description = "General conversation and tool-using assistant"

    def __init__(self):
        self.orchestrator = Orchestrator()

    async def handle(
        self, message: str, context: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        history: List[Dict] = (context or {}).get("history", [])
        async for event in self.orchestrator.run(message, history=history):
            yield event
