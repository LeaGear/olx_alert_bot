import os


TOKEN = os.getenv("TOKEN")

DATA_FILE = "data_store/users_subs_data.json"
KEYBOARDS = {
    "my_subscribes": "🗒 Мои подписки",
    "add_subscribe": "🟢 Добавить подписку",
    "delete_subscribe": "🔴 Удалить подписку",
    "properties": "⚙️ Настройки",
    "menu": "↩️ Назад в меню"
}

BACKEND_URL = "http://127.0.0.1:8000"

API_VERSION = "/v1"

API_COMMANDS = {
    "add_sub" : f"{API_VERSION}/subscriptions/add",
    "get_user_subs" : f"{API_VERSION}/subscriptions/{{}}",
    "delete_sub" : f"{API_VERSION}/subscriptions/{{}}/delete/{{}}",
}
