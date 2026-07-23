import requests
import json
import os
import time

URL = "https://госавтоинспекция.рф/upload/site25/division_service/link/Grafik_Iyul_vse.pdf"

STATE_FILE = "files.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"files": {}}


def save_state(data):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


while True:
    print("START CHECK", flush=True)

    old_state = load_state()

    try:
        r = requests.get(
            URL,
            timeout=60,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        size = len(r.content)

        print("STATUS:", r.status_code, flush=True)
        print("SIZE:", size, flush=True)

        new_state = {
            "files": {
                "Grafik_Iyul_vse.pdf": {
                    "size": size
                }
            }
        }

        if old_state != new_state:
            print("CHANGE DETECTED", flush=True)
            save_state(new_state)
        else:
            print("NO CHANGES", flush=True)

    except Exception as e:
        print("ERROR:", e, flush=True)

    print("WAIT 1 HOUR", flush=True)

    time.sleep(3600)