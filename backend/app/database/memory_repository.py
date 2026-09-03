from datetime import datetime
from typing import Optional, List
from sqlalchemy import select, update, desc
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import MemoryItem, Conversation, Message
from app.utils.logger import logger
import json


class MemoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_memory(
        self,
        content: str,
        key: Optional[str] = None,
        category: str = "general",
        importance: float = 0.5,
        embedding: Optional[List[float]] = None,
    ) -> MemoryItem:
        item = MemoryItem(
            key=key or content[:80],
            content=content,
            category=category,
            importance=importance,
            embedding=json.dumps(embedding) if embedding else None,
        )
        self.session.add(item)
        await self.session.commit()
        await self.session.refresh(item)
        logger.info(f"Memory stored: {item.key[:50]}...")
        return item

    async def search_memories(
        self, query: str, limit: int = 10, category: Optional[str] = None
    ) -> List[MemoryItem]:
        stmt = select(MemoryItem).order_by(desc(MemoryItem.importance), desc(MemoryItem.last_accessed))
        if category:
            stmt = stmt.where(MemoryItem.category == category)
        result = await self.session.execute(stmt.limit(limit * 3))
        items = result.scalars().all()
        query_lower = query.lower()
        scored = []
        for item in items:
            score = 0
            if query_lower in item.content.lower():
                score += 2
            if item.key and query_lower in item.key.lower():
                score += 3
            if score > 0:
                scored.append((score, item))
        scored.sort(key=lambda x: -x[0])
        return [i for _, i in scored[:limit]]

    async def get_recent_memories(self, limit: int = 20) -> List[MemoryItem]:
        stmt = select(MemoryItem).order_by(desc(MemoryItem.created_at)).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def touch_memory(self, memory_id: int):
        await self.session.execute(
            update(MemoryItem)
            .where(MemoryItem.id == memory_id)
            .values(
                last_accessed=datetime.utcnow(),
                access_count=MemoryItem.access_count + 1,
            )
        )
        await self.session.commit()

    async def create_conversation(self, title: str = "New Conversation") -> Conversation:
        conv = Conversation(title=title)
        self.session.add(conv)
        await self.session.commit()
        await self.session.refresh(conv)
        return conv

    async def add_message(
        self, conversation_id: int, role: str, content: str, tool_calls: Optional[str] = None
    ) -> Message:
        msg = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_calls=tool_calls,
        )
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def get_conversation_messages(self, conversation_id: int, limit: int = 50) -> List[Message]:
        stmt = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
