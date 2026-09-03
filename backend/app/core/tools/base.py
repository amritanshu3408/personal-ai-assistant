from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.utils.logger import logger


class ToolResult(BaseModel):
    success: bool
    data: Any = None
    error: Optional[str] = None
    message: str = ""


class BaseTool(ABC):
    name: str
    description: str
    parameters: Dict[str, Any]  # JSON Schema style

    def to_openai_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult:
        ...

    async def safe_execute(self, **kwargs) -> ToolResult:
        try:
            logger.info(f"Executing tool {self.name} with {kwargs}")
            result = await self.execute(**kwargs)
            return result
        except Exception as e:
            logger.exception(f"Tool {self.name} failed")
            return ToolResult(success=False, error=str(e), message=f"Tool failed: {e}")
