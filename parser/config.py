import os


BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

REFRESH_INTERVAL = 2
SERVER_TIMEOUT = 5
API_VERSION = "/v1"

API_REQUESTS = {
    "get_subs" : API_VERSION + "/parser/get_all_users_subs",
    "post_subs" : API_VERSION + "/parser/update_users_subs"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
}

QUERY_PARAMS = "search%5Border%5D=created_at:desc"