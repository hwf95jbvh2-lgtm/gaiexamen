import requests

URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"
SEARCH = "График проведения экзаменов на Август 2026"

BOT_TOKEN = "ВСТАВЬ_НОВЫЙ_ТОКЕН"
CHAT_ID = "448539895"


def send(text):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": text
        }
    )


page = requests.get(URL, timeout=30).text

if SEARCH.lower() in page.lower():
    send(f"✅ На сайте появился файл:\n\n{SEARCH}\n\n{URL}")
    print("FOUND")
else:
    print("NOT FOUND")