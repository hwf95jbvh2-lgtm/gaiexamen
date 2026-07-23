import requests
import time


print("НОВЫЙ BOT.PY ЗАПУЩЕН", flush=True)


BOT_TOKEN = "ТВОЙ_ТОКЕН_БОТА"

CHAT_ID = "ТВОЙ_CHAT_ID"


def send_message(text):

    try:

        response = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={
                "chat_id": CHAT_ID,
                "text": text
            },
            timeout=30
        )

        print(
            "TELEGRAM RESPONSE:",
            response.text,
            flush=True
        )

    except Exception as e:

        print(
            "TELEGRAM ERROR:",
            e,
            flush=True
        )


send_message(
    "✅ Новый бот запущен и работает"
)


while True:

    print(
        "БОТ РАБОТАЕТ",
        flush=True
    )

    time.sleep(60)