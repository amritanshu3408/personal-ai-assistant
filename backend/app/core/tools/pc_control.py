import asyncio
import os
import subprocess
import platform
from typing import Optional
from app.core.tools.base import BaseTool, ToolResult
from app.utils.logger import logger

try:
    import pyautogui
    import pyperclip
    HAS_GUI = True
except ImportError:
    HAS_GUI = False


class OpenApplicationTool(BaseTool):
    name = "open_application"
    description = "Open an application or file on the user's PC by name or path."
    parameters = {
        "type": "object",
        "properties": {
            "name_or_path": {
                "type": "string",
                "description": "Application name (e.g. 'notepad', 'chrome') or full path",
            }
        },
        "required": ["name_or_path"],
    }

    async def execute(self, name_or_path: str) -> ToolResult:
        system = platform.system()
        try:
            if system == "Windows":
                common = {
                    "notepad": "notepad.exe",
                    "calculator": "calc.exe",
                    "explorer": "explorer.exe",
                    "cmd": "cmd.exe",
                    "powershell": "powershell.exe",
                    "chrome": "chrome",
                    "edge": "msedge",
                    "firefox": "firefox",
                }
                target = common.get(name_or_path.lower(), name_or_path)
                subprocess.Popen(target, shell=True)
            elif system == "Darwin":
                subprocess.Popen(["open", "-a", name_or_path])
            else:
                subprocess.Popen([name_or_path])
            return ToolResult(success=True, message=f"Opened {name_or_path}")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class RunCommandTool(BaseTool):
    name = "run_shell_command"
    description = "Run a safe shell command and return stdout/stderr. Use with caution."
    parameters = {
        "type": "object",
        "properties": {
            "command": {"type": "string", "description": "Command to run"},
            "timeout": {"type": "number", "description": "Timeout seconds", "default": 30},
        },
        "required": ["command"],
    }

    BLOCKED = ["rm -rf", "format", "del /s", "shutdown", "reboot", "mkfs", ":(){:|:&};:"]

    async def execute(self, command: str, timeout: float = 30) -> ToolResult:
        lower = command.lower()
        for b in self.BLOCKED:
            if b in lower:
                return ToolResult(success=False, error="Command blocked for safety")
        try:
            proc = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await asyncio.wait_for(proc.communicate(), timeout=timeout)
            return ToolResult(
                success=proc.returncode == 0,
                data={
                    "stdout": stdout.decode(errors="replace")[:4000],
                    "stderr": stderr.decode(errors="replace")[:2000],
                    "returncode": proc.returncode,
                },
                message="Command executed",
            )
        except asyncio.TimeoutError:
            return ToolResult(success=False, error="Command timed out")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class TypeTextTool(BaseTool):
    name = "type_text"
    description = "Type text into the currently focused window (keyboard simulation)."
    parameters = {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "interval": {"type": "number", "default": 0.02},
        },
        "required": ["text"],
    }

    async def execute(self, text: str, interval: float = 0.02) -> ToolResult:
        if not HAS_GUI:
            return ToolResult(success=False, error="GUI automation not available")
        try:
            await asyncio.to_thread(pyautogui.write, text, interval=interval)
            return ToolResult(success=True, message="Text typed")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class GetClipboardTool(BaseTool):
    name = "get_clipboard"
    description = "Read the current clipboard content."
    parameters = {"type": "object", "properties": {}}

    async def execute(self) -> ToolResult:
        if not HAS_GUI:
            return ToolResult(success=False, error="Clipboard access not available")
        try:
            content = await asyncio.to_thread(pyperclip.paste)
            return ToolResult(success=True, data=content, message="Clipboard read")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class SetClipboardTool(BaseTool):
    name = "set_clipboard"
    description = "Set the system clipboard content."
    parameters = {
        "type": "object",
        "properties": {"text": {"type": "string"}},
        "required": ["text"],
    }

    async def execute(self, text: str) -> ToolResult:
        if not HAS_GUI:
            return ToolResult(success=False, error="Clipboard access not available")
        try:
            await asyncio.to_thread(pyperclip.copy, text)
            return ToolResult(success=True, message="Clipboard set")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


PC_TOOLS = [
    OpenApplicationTool(),
    RunCommandTool(),
    TypeTextTool(),
    GetClipboardTool(),
    SetClipboardTool(),
]
