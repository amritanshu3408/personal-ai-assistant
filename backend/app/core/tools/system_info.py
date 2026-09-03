import platform
import psutil
from datetime import datetime
from app.core.tools.base import BaseTool, ToolResult


class GetSystemInfoTool(BaseTool):
    name = "get_system_info"
    description = "Get basic system information: OS, CPU, memory, disk, uptime."
    parameters = {"type": "object", "properties": {}}

    async def execute(self) -> ToolResult:
        try:
            boot = datetime.fromtimestamp(psutil.boot_time())
            mem = psutil.virtual_memory()
            disk = psutil.disk_usage("/")
            info = {
                "os": platform.system(),
                "os_version": platform.version(),
                "architecture": platform.machine(),
                "hostname": platform.node(),
                "cpu_count": psutil.cpu_count(logical=True),
                "cpu_percent": psutil.cpu_percent(interval=0.5),
                "memory_total_gb": round(mem.total / (1024**3), 2),
                "memory_used_gb": round(mem.used / (1024**3), 2),
                "memory_percent": mem.percent,
                "disk_total_gb": round(disk.total / (1024**3), 2),
                "disk_used_gb": round(disk.used / (1024**3), 2),
                "disk_percent": disk.percent,
                "boot_time": boot.isoformat(),
            }
            return ToolResult(success=True, data=info, message="System info retrieved")
        except Exception as e:
            return ToolResult(success=False, error=str(e))


class ListProcessesTool(BaseTool):
    name = "list_processes"
    description = "List top processes by CPU or memory usage."
    parameters = {
        "type": "object",
        "properties": {
            "sort_by": {"type": "string", "enum": ["cpu", "memory"], "default": "cpu"},
            "limit": {"type": "integer", "default": 10},
        },
    }

    async def execute(self, sort_by: str = "cpu", limit: int = 10) -> ToolResult:
        try:
            procs = []
            for p in psutil.process_iter(["pid", "name", "cpu_percent", "memory_percent"]):
                try:
                    info = p.info
                    procs.append(info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            key = "cpu_percent" if sort_by == "cpu" else "memory_percent"
            procs.sort(key=lambda x: x.get(key) or 0, reverse=True)
            return ToolResult(
                success=True,
                data=procs[:limit],
                message=f"Top {limit} processes by {sort_by}",
            )
        except Exception as e:
            return ToolResult(success=False, error=str(e))


SYSTEM_TOOLS = [GetSystemInfoTool(), ListProcessesTool()]
