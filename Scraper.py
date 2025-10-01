# scraper.py
import requests
from bs4 import BeautifulSoup
import random   # <-- new

URL = "https://en.wikipedia.org/wiki/List_of_legendary_creatures_by_type"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def scrape_wiki_creatures():
    """Return a shuffled list of creature names from the Wikipedia page."""
    r = requests.get(URL, headers=HEADERS, timeout=20)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    content = soup.find(id="mw-content-text")
    if not content:
        return []

    names = set()
    for li in content.select("li"):
        a = li.find("a", href=True)
        if not a:
            continue
        href = a["href"]
        text = a.get_text(strip=True)
        if not href.startswith("/wiki/"):
            continue
        if ":" in href:               # skip Help:, File:, Category:, etc.
            continue
        if not text or text.lower().startswith("list of"):
            continue
        names.add(text)

    names_list = list(names)
    random.shuffle(names_list)   # shuffle order each run
    return names_list

def run_scrape_and_print(limit=50):
    """Helper used by main.py to actually print results in random order."""
    names = scrape_wiki_creatures()
    if not names:
        print("❌ No creature names found.")
        return
    print(f"\n✅ Random sample of {limit} creatures (from {len(names)} total):\n")
    for i, name in enumerate(names[:limit], start=1):
        print("-", i, ":", name)

