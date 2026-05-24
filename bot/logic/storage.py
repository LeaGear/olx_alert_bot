import os
import asyncio
import aiofiles
import json

from bot.data.config import DATA_FILE

_data_cache = {}  # Private data cache
_save_lock = None


async def load_file(file_name):
    try:
        async with aiofiles.open(file_name, mode="r", encoding="utf-8") as f:
            contents = await f.read()
            return json.loads(contents)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


async def save_file(data, file_name=DATA_FILE):
    global _save_lock

    if not _save_lock: _save_lock = asyncio.Lock()

    async with _save_lock:
        async with aiofiles.open(file_name, "w", encoding="utf-8") as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=4))
    print("File saved!")


def check_data_file():
    if os.path.exists(DATA_FILE):
        pass

    else:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            f.write("{}")


def get_actual_cache():  # Getter function for receiving actual cache
    return _data_cache


async def caching_users_data():
    global _data_cache

    _data_cache = await load_file(DATA_FILE)
