"""Find every pair of KBO players whose registered names can be spliced:

    player A's last two characters == player B's first two characters
    e.g. 최원태 + 원태인 -> 최원태인 (원태 overlaps)
        에레디아 + 디아즈 -> 에레디아즈 (디아 overlaps)

Names of 2 characters or fewer are excluded: a 2-character name is entirely
consumed by the overlap, so the "merged" result is just the other player's
name verbatim rather than a genuine splice.

Matching is done at the player level (not just unique name strings) so that
homonyms -- different real players who share a registered name -- each
produce their own row with their own team/status/nationality, and so the
UI's team/status/nationality filters have real per-player data to filter on.

Reads data/players.json (produced by scrape.py) and writes data/payload.json,
the exact JSON payload the page template embeds and renders client-side.
"""
import json
from collections import defaultdict

IN_PATH = "data/players.json"
OUT_PATH = "data/payload.json"


def status_bucket(p):
    s = p.get("status")
    if s == "active":
        return "active"
    if s == "retired":
        return "retired"
    return "other"  # prospect (육성선수) / unknown


def main():
    data = json.load(open(IN_PATH, encoding="utf-8"))
    all_players = data["data"]

    # Names of length <= 2 are excluded entirely -- see module docstring.
    players = [p for p in all_players if len(p["name"]) >= 3]

    by_prefix = defaultdict(list)
    for p in players:
        by_prefix[p["name"][:2]].append(p)

    rows = []
    unique_pairs = set()
    for a in players:
        tail = a["name"][-2:]
        for b in by_prefix.get(tail, []):
            if a["name"] == b["name"]:
                continue
            merged = a["name"][:-2] + b["name"]
            unique_pairs.add((a["name"], b["name"]))
            rows.append({
                "a": a["name"], "b": b["name"], "m": merged,
                "ap": a["name"][:-2], "st": tail, "bs": b["name"][2:],
                "aId": a["id"], "bId": b["id"],
                "aTeam": a.get("team_name"), "bTeam": b.get("team_name"),
                "aStatus": status_bucket(a), "bStatus": status_bucket(b),
                "aForeign": bool(a.get("is_foreign")), "bForeign": bool(b.get("is_foreign")),
            })

    payload = {
        "meta": {
            "total_players": data["pagination"]["total"],
            "eligible_players": len(players),
            "unique_names": len(set(p["name"] for p in players)),
            "unique_pairs": len(unique_pairs),
            "total_rows": len(rows),
        },
        "rows": rows,
    }

    print(payload["meta"])
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, separators=(",", ":"))
    print(f"saved {len(rows)} rows to {OUT_PATH}")


if __name__ == "__main__":
    main()
