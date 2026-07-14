"""Fetch the full KBO player list from yagoonara.com's internal API.

The site's /players/search page is a Next.js app that loads data client-side
from /api/players. That endpoint accepts a `limit` param large enough to
return every player in a single request, so no pagination loop is needed.
"""
import json
import urllib.request

API_URL = "https://www.yagoonara.com/api/players?page=1&limit=10000"
OUT_PATH = "data/players.json"

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"


def main():
    req = urllib.request.Request(API_URL, headers={"User-Agent": UA})
    with urllib.request.urlopen(req) as resp:
        data = json.load(resp)

    print("total players:", data["pagination"]["total"])
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"saved {len(data['data'])} players to {OUT_PATH}")


if __name__ == "__main__":
    main()
