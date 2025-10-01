import os, requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("SERPER_API_KEY")

def serper_search(query):
    if not API_KEY:
        print("❌ Missing SERPER_API_KEY in .env")
        return

    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": API_KEY, "Content-Type": "application/json"}
    payload = {"q": query, "num": 10}

    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    if resp.status_code == 401:
        print("❌ Unauthorized: check your key")
        return
    resp.raise_for_status()

    data = resp.json()
    items = data.get("organic", []) or data.get("results", [])
    print("\n✅ Search results:")
    count = 1
    for item in items:
        print("-", count,". ", item.get("title"), ":", item.get("link"))
        print(item.get("snippet") or "")
        print("------")
        count += 1