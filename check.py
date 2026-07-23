import requests
from bs4 import BeautifulSoup
import json
import os
import time


PAGE_URL = "https://госавтоинспекция.рф/svc/273"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

CHECK_INTERVAL = 3600  # 1 час

DATA_FILE = "files.json"


def send_message(text):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram settings are missing")
        return

    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        },
        timeout=30
    )


def load_old_files():
    if not os.path.exists(DATA_FILE):
        return []

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_files(files):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(files, f, ensure_ascii=False, indent=2)


def get_files():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(
        PAGE_URL,
        headers=headers,
        timeout=60
    )

    r.raise_for_status()

    soup = BeautifulSoup(r.text, "html.parser")

    files = []

    for link in soup.find_all("a", href=True):
        href = link["href"]

        if ".pdf" in href.lower():
            name = link.text.strip()

            if not name:
                name = href.split("/")[-1]

            if href.startswith("/"):
                href = "https://госавтоинспекция.рф" + href

            files.append({
                "name": name,
                "url": href
            })

    return files


def check():
    print("Checking files...")

    try:
        current_files = get_files()

        old_files = load_old_files()

        old_urls = {
            x["url"] for x in old_files
        }

        new_files = [
            x for x in current_files
            if x["url"] not in old_urls
        ]

        if new_files:
            message = "🚗 Новый файл на сайте ГИБДД:\n\n"

            for file in new_files:
                message += (
                    f"📄 {file['name']}\n"
                    f"{file['url']}\n\n"
                )

            send_message(message)

            print("New files found")

        else:
            print("No new files")

        save_files(current_files)

    except Exception as e:
        print("ERROR:", e)


while True:
    check()
    time.sleep(CHECK_INTERVAL)