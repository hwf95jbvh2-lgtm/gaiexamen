import requests
from bs4 import BeautifulSoup
import json
import time
import os
from urllib.parse import urljoin


print("VERSION TEST 23-07-15-30", flush=True)


URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

STATE_FILE = "files.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


print(
    "BOT TOKEN EXISTS:",
    bool(BOT_TOKEN),
    flush=True
)

print(
    "CHAT ID:",
    CHAT_ID,
    flush=True
)


def send_message(text):

    if not BOT_TOKEN:
        print(
            "BOT TOKEN MISSING",
            flush=True
        )
        return

    if not CHAT_ID:
        print(
            "CHAT ID MISSING",
            flush=True
        )
        return


    try:

        print(
            "SENDING TELEGRAM...",
            flush=True
        )


        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=15
        )


        print(
            "TELEGRAM RESPONSE:",
            response.status_code,
            response.text,
            flush=True
        )


    except Exception as e:

        print(
            "TELEGRAM ERROR:",
            e,
            flush=True
        )



def load_files():

    if os.path.exists(STATE_FILE):

        try:

            with open(
                STATE_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file).get(
                    "files",
                    []
                )

        except Exception:

            return []

    return []



def save_files(files):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            {
                "files": files
            },
            file,
            ensure_ascii=False,
            indent=2
        )



# тест Telegram при запуске
send_message(
    "✅ Тест: бот запущен"
)



while True:

    print(
        "START CHECK",
        flush=True
    )


    try:

        response = requests.get(
            URL,
            timeout=120,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )


        print(
            "SITE STATUS:",
            response.status_code,
            flush=True
        )


        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )


        current_files = []


        for link in soup.find_all(
            "a",
            href=True
        ):

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

                name = link.text.strip()


                if not name:

                    name = href.split("/")[-1]


                current_files.append(
                    {
                        "name": name,
                        "url": urljoin(
                            URL,
                            href
                        )
                    }
                )



        old_files = load_files()


        old_urls = {
            x["url"]
            for x in old_files
        }


        new_files = [
            x
            for x in current_files
            if x["url"] not in old_urls
        ]



        if new_files:

            message = (
                "📄 Новые файлы ГИБДД:\n\n"
            )


            for file in new_files:

                message += (
                    f"{file['name']}\n"
                    f"{file['url']}\n\n"
                )


            send_message(
                message
            )


            print(
                "NEW FILES SENT",
                flush=True
            )


        else:

            print(
                "NO CHANGES",
                flush=True
            )


        save_files(
            current_files
        )


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


    time.sleep(
        3600
    )