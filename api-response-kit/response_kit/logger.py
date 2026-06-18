import os
import sys
import asyncio
import colorlog
import functools
import logging

from logging.handlers import RotatingFileHandler


os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("main_logger")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s - %(name)s - %(levelname)-8s%(reset)s - %(message)s",
        log_colors = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        os.path.join("logs", 'app.log'),
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8"
    )

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

def log_function(func):
    if asyncio.iscoroutinefunction(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            logger.info(f"Starting function - <<{func.__name__}>> with args - {args}, kwargs - {kwargs}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Successfully finished function - <<{func.__name__}>>")
                return result
            except Exception as e:
                logger.error(f"Critical error in function - <<{func.__name__}>>. Error: {e}", exc_info=True)
                return None
        return wrapper
    else:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger.info(f"Starting function - <<{func.__name__}>> with args - {args}, kwargs - {kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Successfully finished function - <<{func.__name__}>>")
                return result
            except Exception as e:
                logger.error(f"Critical error in function - <<{func.__name__}>>. Error: {e}", exc_info=True)
                return None
        return wrapper