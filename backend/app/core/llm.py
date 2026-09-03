from typing import List, Dict, Any, Optional, AsyncGenerator
from openai import AsyncOpenAI
from app.config import get_settings
from app.utils.logger import logger

settings = get_settings()


def get_client() -> AsyncOpenAI:
    kwargs = {"api_key": settings.openai_api_key or "sk-placeholder"}
    if settings.openai_base_url:
        kwargs["base_url"] = settings.openai_base_url
    return AsyncOpenAI(**kwargs)


async def chat_completion(
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict]] = None,
    tool_choice: str = "auto",
    stream: bool = False,
    temperature: float = 0.7,
) -> Any:
    client = get_client()
    kwargs = {
        "model": settings.openai_model,
        "messages": messages,
        "temperature": temperature,
        "stream": stream,
    }
    if tools:
        kwargs["tools"] = tools
        kwargs["tool_choice"] = tool_choice

    logger.debug(f"LLM call – model={settings.openai_model} tools={bool(tools)}")
    return await client.chat.completions.create(**kwargs)


async def stream_chat(
    messages: List[Dict[str, Any]],
    tools: Optional[List[Dict]] = None,
) -> AsyncGenerator[str, None]:
    response = await chat_completion(messages, tools=tools, stream=True)
    async for chunk in response:
        delta = chunk.choices[0].delta
        if delta.content:
            yield delta.content
