import requests
from bs4 import BeautifulSoup

URL = "https://xn--80aebkobnwfcnsfk1e0h.xn--p1ai/svc/273"

response = requests.get(
    URL,
    timeout=60,
    headers={
        "User-Agent": "Mozilla/5.0"
    }
)

soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a"):
    href = link.get("href")
    text = link.text.strip()

    if href:
        print(text, "→", href)