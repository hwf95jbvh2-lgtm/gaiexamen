import requests
import time

URL = "https://госавтоинспекция.рф/upload/site25/division_service/link/Grafik_Iyul_vse.pdf"

while True:
    print("START CHECK", flush=True)

    try:
        r = requests.get(
            URL,
            timeout=60,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        print("STATUS:", r.status_code, flush=True)
        print("SIZE:", len(r.content), flush=True)

    except Exception as e:
        print("ERROR:", e, flush=True)

    print("WAIT 1 HOUR", flush=True)
    time.sleep(3600)