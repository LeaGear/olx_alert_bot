import os
#import pytz

from dotenv import load_dotenv

load_dotenv("data/.env")

TOKEN = os.getenv("TOKEN")

RATE_LIMIT = 0.05
REFRESH_INTERVAL = 5 #minutes
REFRESH_INTERVAL_ALERT = 1 #minute

DATA_FILE = "data/users_subs_data.json"
KEYBOARDS = {
    "my_subscribes" : "🗒 Мои подписки!",
    "add_subscribe" : "🟢 Добавить подписку!",
    "delete_subscribe" : "🔴 Удалить подписку",
    "properties" : "⚙️ Настройки",
    "menu" : "Back to Menu!"
}