import os

from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

REFRESH_INTERVAL = 2
SERVER_TIMEOUT = 5
API_VERSION = "/v1"

API_REQUESTS = {
    "get_subs": API_VERSION + "/parser/get_all_users_subs",
    "post_subs": API_VERSION + "/parser/update_users_subs"
}

HEADERS_RESERVE = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7"
}

HEADERS = {
    # Main header - real browser
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",

    # response content - JSON
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",

    # Language
    "Accept-Language": "uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7",

    "Accept-Encoding": "gzip, deflate",

    "Referer": "https://www.olx.ua/",

    "Sec-Ch-Ua": '"Google Chrome";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"macOS"',

    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",

    "Cache-Control": "max-age=0",
    "Upgrade-Insecure-Requests": "1"
}

QUERY_PARAMS = "search%5Border%5D=created_at:desc"

TIME_DIFFERENCE = 3