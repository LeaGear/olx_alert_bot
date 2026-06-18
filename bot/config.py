import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")


KEYBOARDS = {
    "my_subscribes": "🗒 Мои подписки",
    "add_subscribe": "🟢 Добавить подписку",
    "delete_subscribe": "🔴 Удалить подписку",
    "properties": "⚙️ Настройки",
    "menu": "↩️ Назад в меню"
}

SERVER_TIMEOUT = 5


API_VERSION = "/v1"

API_COMMANDS = {
    "add_sub" : API_VERSION + "/subscriptions/add",
    "get_user_subs" : API_VERSION + "/subscriptions/{}",
    "delete_sub" : API_VERSION + "/subscriptions/{}/delete/{}",
}
