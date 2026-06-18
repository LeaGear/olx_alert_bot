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

    #function to dave space in logs
    def clean_arg(arg):
        if isinstance(arg, dict):
            if len(arg) > 5:
                return f"[Dict with {len(arg)} keys (hidden to save space)]"
            return arg
        elif isinstance(arg, list):
            if len(arg) > 5:
                return f"[List with {len(arg)} items (hidden to save space)]"
            return arg
        elif isinstance(arg, str) and len(arg) > 200:
            return f"{arg[:100]}... [Truncated, total length: {len(arg)}]"
        return arg

    #Check for async or sync function
    if asyncio.iscoroutinefunction(func):

        #Handler if async function
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            cleaned_args = [clean_arg(a) for a in args]
            cleaned_kwargs = {k: clean_arg(v) for k, v in kwargs.items()}

            logger.info(f"Starting function - <<{func.__name__}>> with args - {cleaned_args}, kwargs - {cleaned_kwargs}")
            try:
                result = await func(*args, **kwargs)
                logger.info(f"Successfully finished function - <<{func.__name__}>>")
                return result
            except Exception as e:
                logger.error(f"Critical error in function - <<{func.__name__}>>. Error: {e}", exc_info=True)
                return None
        return wrapper
    else:
        #HAndler if function - sync
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            cleaned_args = [clean_arg(a) for a in args]
            cleaned_kwargs = {k: clean_arg(v) for k, v in kwargs.items()}

            logger.info(f"Starting function - <<{func.__name__}>> with args - {cleaned_args}, kwargs - {cleaned_kwargs}")
            try:
                result = func(*args, **kwargs)
                logger.info(f"Successfully finished function - <<{func.__name__}>>")
                return result
            except Exception as e:
                logger.error(f"Critical error in function - <<{func.__name__}>>. Error: {e}", exc_info=True)
                return None
        return wrapper