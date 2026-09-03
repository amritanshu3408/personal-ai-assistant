import json
from typing import List, Dict, Any, Optional, AsyncGenerator
from app.core.llm import chat_completion
from app.core.tools import get_openai_tools, TOOL_MAP
from app.utils.logger import logger

SYSTEM_PROMPT = """You are a helpful personal AI assistant running on the user's computer.
You have tools to control the PC, browse the web, get system info, and remember/recall information.
Be concise, proactive, and confirm before destructive actions.
When using tools, explain briefly what you are doing.
Current date context is available from the system.
"""


class Orchestrator:
    def __init__(self, max_tool_rounds: int = 6):
        self.max_tool_rounds = max_tool_rounds
        self.tools = get_openai_tools()

    async def run(
        self,
        user_message: str,
        history: Optional[List[Dict[str, Any]]] = None,
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Yields events:
          {"type": "token", "content": "..."}
          {"type": "tool_call", "name": "...", "args": {...}}
          {"type": "tool_result", "name": "...", "result": {...}}
          {"type": "final", "content": "..."}
          {"type": "error", "message": "..."}
        """
        messages: List[Dict[str, Any]] = [
            {"role": "system", "content": SYSTEM_PROMPT},
        ]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        for round_idx in range(self.max_tool_rounds):
            try:
                response = await chat_completion(
                    messages, tools=self.tools, stream=False
                )
            except Exception as e:
                logger.exception("LLM error")
                yield {"type": "error", "message": str(e)}
                return

            choice = response.choices[0]
            msg = choice.message

            # Tool calls?
            if msg.tool_calls:
                # Append assistant message with tool_calls
                messages.append(
                    {
                        "role": "assistant",
                        "content": msg.content or "",
                        "tool_calls": [
                            {
                                "id": tc.id,
                                "type": "function",
                                "function": {
                                    "name": tc.function.name,
                                    "arguments": tc.function.arguments,
                                },
                            }
                            for tc in msg.tool_calls
                        ],
                    }
                )

                for tc in msg.tool_calls:
                    name = tc.function.name
                    try:
                        args = json.loads(tc.function.arguments or "{}")
                    except json.JSONDecodeError:
                        args = {}

                    yield {"type": "tool_call", "name": name, "args": args}

                    tool = TOOL_MAP.get(name)
                    if not tool:
                        result = {"success": False, "error": f"Unknown tool {name}"}
                    else:
                        tool_result = await tool.safe_execute(**args)
                        result = tool_result.model_dump()

                    yield {"type": "tool_result", "name": name, "result": result}

                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tc.id,
                            "content": json.dumps(result, default=str),
                        }
                    )
                continue  # next round

            # Final answer
            content = msg.content or ""
            yield {"type": "final", "content": content}
            return

        yield {
            "type": "final",
            "content": "I reached the maximum number of tool rounds. Please try a simpler request.",
        }
