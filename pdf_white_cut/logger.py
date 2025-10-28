import sys
import os
from pathlib import Path
import loguru

# Default log directory
default_log_dir = Path("logs")
default_log_dir.mkdir(exist_ok=True)

# Get log level from environment variable, default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Console log level (can be overridden by LOG_LEVEL env var)
CONSOLE_LOG_LEVEL = os.getenv("CONSOLE_LOG_LEVEL", LOG_LEVEL)

# Create logger instance
logger = loguru.logger

# Remove default handlers
current_handlers = logger._core.handlers.copy()
for handler_id in current_handlers:
    logger.remove(handler_id)


# Add console handler with better formatting
logger.add(
    sys.stderr,
    level=CONSOLE_LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    colorize=True,
)


def add_file_log():
    # Add file handler for debug logs (always DEBUG level to capture all info)
    logger.add(
        default_log_dir / "debug.log",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        rotation="100 MB",
        retention="7 days",
        compression="zip",
    )

    # Add file handler for error logs
    logger.add(
        default_log_dir / "error.log",
        level="ERROR",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}\n{exception}",
        rotation="100 MB",
        retention="7 days",
        compression="zip",
    )


# Export the logger instance
__all__ = ["logger", "add_file_log"]
