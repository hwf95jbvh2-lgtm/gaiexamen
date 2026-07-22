import requests

URL = "https://госавтоинспекция.рф/upload/site25/division_service/link/Grafik_Iyul_vse.pdf"

r = requests.get(
    URL,
    timeout=30,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("STATUS:", r.status_code)
print("SIZE:", len(r.content))