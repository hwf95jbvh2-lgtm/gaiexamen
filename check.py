import requests
import json
import time
import os
from bs4 import BeautifulSoup

URL = "https://госавтоинспекция.рф/svc/273"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

STATE_FILE = "files.json"


def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


def get_files():
    r = requests.get(
        URL,
        timeout=60,
        headers={
            "User-Agent": "Mozilla/5.0"
        }
    )

    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    files = []

    for link in soup.find_all("a"):
        href = link.get("href")

        if href and ".pdf" in href.lower():
            name = link.text.strip()

            if name:
                files.append(name)

    return sorted(files)


def load_old():
    try:
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_new(files):
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


while True:

    try:
        current = get_files()
        old = load_old()

        if old:
            new_files = [
                f for f in current
                if f not in old
            ]

            if new_files:
                message = "✅ На сайте появились новые файлы:\n\n"

                for f in new_files:
                    message += f"📄 {f}\n"

                message += f"\n{URL}"

                send(message)

        save_new(current)

        print(
            "Проверка выполнена:",
            len(current),
            "файлов"
        )

    except Exception as e:
        print("Ошибка:", e)

    time.sleep(3600)