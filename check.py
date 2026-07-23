import requests
from bs4 import BeautifulSoup
import json
import time
import os

URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

STATE_FILE = "files.json"


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

        print("STATUS:", r.status_code, flush=True)

        soup = BeautifulSoup(r.text, "html.parser")

        files = []

        for link in soup.find_all("a", href=True):
            href = link["href"]

            if any(
                ext in href.lower()
                for ext in [".pdf", ".doc", ".docx", ".xls", ".xlsx"]
            ):
                files.append(href)

        files = sorted(files)

        print("FILES FOUND:", len(files), flush=True)

        old_files = load_files()

        if files != old_files:
            print("CHANGE DETECTED", flush=True)
            print("OLD:", old_files, flush=True)
            print("NEW:", files, flush=True)

            save_files(files)

        else:
            print("NO CHANGES", flush=True)

    except Exception as e:
        print("ERROR:", e, flush=True)

    print("WAIT 1 HOUR", flush=True)

    time.sleep(3600)