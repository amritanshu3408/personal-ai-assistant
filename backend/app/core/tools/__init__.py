from app.core.tools.pc_control import PC_TOOLS
from app.core.tools.system_info import SYSTEM_TOOLS
from app.core.tools.browser import BROWSER_TOOLS
from app.core.tools.memory import MEMORY_TOOLS
from app.core.tools.base import BaseTool

ALL_TOOLS: list[BaseTool] = [
    *PC_TOOLS,
    *SYSTEM_TOOLS,
    *BROWSER_TOOLS,
    *MEMORY_TOOLS,
]

TOOL_MAP = {t.name: t for t in ALL_TOOLS}


def get_openai_tools() -> list[dict]:
    return [t.to_openai_schema() for t in ALL_TOOLS]
