import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin


URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

STATE_FILE = "/data/files.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram settings missing", flush=True)
        return

    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=30
        )

        print("TELEGRAM SENT", flush=True)

    except Exception as e:
        print("TELEGRAM ERROR:", e, flush=True)


def load_files():
    if not os.path.exists(STATE_FILE):
        return []

    try:
        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:
            return json.load(f)

    except:
        return []


def save_files(files):
    os.makedirs(
        "/data",
        exist_ok=True
    )

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(
            files,
            f,
            ensure_ascii=False,
            indent=2
        )


def check():

    print("START CHECK", flush=True)

    response = requests.get(
        URL,
        timeout=60,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    files = []

    for link in soup.find_all(
        "a",
        href=True
    ):

        href = link["href"]

        if any(
            x in href.lower()
            for x in [
                ".pdf",
                ".doc",
                ".docx",
                ".xls",
                ".xlsx"
            ]
        ):

            name = link.text.strip()

            if not name:
                name = href.split("/")[-1]

            files.append(
                {
                    "name": name,
                    "url": urljoin(URL, href)
                }
            )


    old_files = load_files()


    old_urls = {
        x["url"]
        for x in old_files
    }


    new_files = [
        x for x in files
        if x["url"] not in old_urls
    ]


    if new_files and old_files:

        text = "📄 Новые файлы ГИБДД:\n\n"

        for f in new_files:
            text += (
                f"{f['name']}\n"
                f"{f['url']}\n\n"
            )

        send_message(text)


    elif not old_files:

        send_message(
            "✅ Бот запущен. Первичная проверка выполнена."
        )


    else:

        print(
            "NO CHANGES",
            flush=True
        )


    save_files(files)


while True:

    try:
        check()

    except Exception as e:

        print(
            "ERROR:",
            e,
            flush=True
        )

    print(
        "WAIT 1 HOUR",
        flush=True
    )

    time.sleep(3600)