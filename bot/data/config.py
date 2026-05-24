import os

from dotenv import load_dotenv

load_dotenv("data/.env")

TOKEN = os.getenv("TOKEN")

RATE_LIMIT = 0.05
REFRESH_INTERVAL = 5  # minutes
REFRESH_INTERVAL_ALERT = 1  # minute

DATA_FILE = "data/users_subs_data.json"
KEYBOARDS = {
    "my_subscribes": "🗒 Мои подписки",
    "add_subscribe": "🟢 Добавить подписку",
    "delete_subscribe": "🔴 Удалить подписку",
    "properties": "⚙️ Настройки",
    "menu": "↩️ Назад к меню"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
}

QUERY_PARAMS = "search%5Border%5D=created_at:desc"
