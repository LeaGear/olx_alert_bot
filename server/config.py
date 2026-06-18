import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/test")
BOT_URL = os.getenv("BOT_URL", "http://127.0.0.1:8001")


API_VERSION = "/v1"


RATE_LIMIT = 0.05
REFRESH_INTERVAL = 5  # minutes
REFRESH_INTERVAL_ALERT = 1  # minute