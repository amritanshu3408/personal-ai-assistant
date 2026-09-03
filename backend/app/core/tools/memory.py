from typing import Optional
from app.core.tools.base import BaseTool, ToolResult
from app.database.database import AsyncSessionLocal
from app.database.memory_repository import MemoryRepository


class RememberTool(BaseTool):
    name = "remember"
    description = "Store a piece of information in long-term memory for future conversations."
    parameters = {
        "type": "object",
        "properties": {
            "content": {"type": "string", "description": "The information to remember"},
            "key": {"type": "string", "description": "Optional short key / title"},
            "category": {"type": "string", "default": "general"},
            "importance": {"type": "number", "default": 0.7, "minimum": 0, "maximum": 1},
        },
        "required": ["content"],
    }

    async def execute(
        self,
        content: str,
        key: Optional[str] = None,
        category: str = "general",
        importance: float = 0.7,
    ) -> ToolResult:
        async with AsyncSessionLocal() as session:
            repo = MemoryRepository(session)
            item = await repo.add_memory(
                content=content, key=key, category=category, importance=importance
            )
            return ToolResult(
                success=True,
                data={"id": item.id, "key": item.key},
                message="Remembered successfully",
            )


class RecallTool(BaseTool):
    name = "recall"
    description = "Search long-term memory for relevant information."
    parameters = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "limit": {"type": "integer", "default": 5},
            "category": {"type": "string"},
        },
        "required": ["query"],
    }

    async def execute(
        self, query: str, limit: int = 5, category: Optional[str] = None
    ) -> ToolResult:
        async with AsyncSessionLocal() as session:
            repo = MemoryRepository(session)
            items = await repo.search_memories(query, limit=limit, category=category)
            data = [
                {
                    "id": i.id,
                    "key": i.key,
                    "content": i.content,
                    "category": i.category,
                    "importance": i.importance,
                }
                for i in items
            ]
            return ToolResult(success=True, data=data, message=f"Found {len(data)} memories")


MEMORY_TOOLS = [RememberTool(), RecallTool()]
