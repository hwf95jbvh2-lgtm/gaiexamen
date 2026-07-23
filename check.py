import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin


raise Exception("НУЖНЫЙ ФАЙЛ ЗАПУЩЕН")


print("VERSION TEST 23-07-15-30", flush=True)


URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

STATE_FILE = "files.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):

    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram settings missing", flush=True)
        return

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        json={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


def load_files():

    if os.path.exists(STATE_FILE):

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f).get(
                "files",
                []
            )

    return []


def save_files(files):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            {
                "files": files
            },
            f,
            ensure_ascii=False,
            indent=2
        )


while True:

    print(
        "START CHECK",
        flush=True
    )

    time.sleep(3600)