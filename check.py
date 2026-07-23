import requests
from bs4 import BeautifulSoup
import json
import time
import os

URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

STATE_FILE = "files.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram settings missing", flush=True)
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(
        url,
        json={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


def load_files():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f).get("files", [])
    return []


def save_files(files):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(
            {"files": files},
            f,
            ensure_ascii=False,
            indent=2
        )


while True:

    print("START CHECK", flush=True)

    try:
        r = requests.get(
            URL,
            timeout=60,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        soup = BeautifulSoup(
            r.text,
            "html.parser"
        )

        files = []

        for link in soup.find_all("a", href=True):
            href = link["href"]

            if any(
                ext in href.lower()
                for ext in [
                    ".pdf",
                    ".doc",
                    ".docx",
                    ".xls",
                    ".xlsx"
                ]
            ):
                files.append(href)

        files = sorted(files)

        old_files = load_files()

        print("FILES:", len(files), flush=True)

        if files != old_files:

            new_files = set(files) - set(old_files)

            message = "Изменения на сайте ГИБДД:\n\n"

            if new_files:
                message += "Новые файлы:\n"
                for f in new_files:
                    message += f + "\n"

            else:
                message += "Изменились существующие файлы"

            send_message(message)

            save_files(files)

            print("MESSAGE SENT", flush=True)

        else:
            print("NO CHANGES", flush=True)

    except Exception as e:
        print("ERROR:", e, flush=True)

    time.sleep(3600)