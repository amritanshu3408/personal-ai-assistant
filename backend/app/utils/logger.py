from loguru import logger
import sys

logger.remove()
logger.add(
    sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
)
logger.add(
    "logs/assistant.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    enqueue=True,
)

__all__ = ["logger"]
