import requests

print("START CHECK", flush=True)

URL = "https://госавтоинспекция.рф/upload/site25/division_service/link/Grafik_Iyul_vse.pdf"

try:
    r = requests.get(
        URL,
        timeout=30,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    print("STATUS:", r.status_code, flush=True)
    print("SIZE:", len(r.content), flush=True)

except Exception as e:
    print("ERROR:", e, flush=True)