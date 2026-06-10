import json
import hashlib
from pathlib import Path
from datetime import datetime, timezone

EDITIONS_DIR = Path("data/editions")
EDITIONS_INDEX = Path("site/src/data/editions_index.json")
CURRENT_JSON = Path("site/src/data/current.json")


def _edition_number() -> int:
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    return len(list(EDITIONS_DIR.glob("*.json"))) + 1


def generate_edition(articles: list[dict], date: str) -> dict:
    EDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    CURRENT_JSON.parent.mkdir(parents=True, exist_ok=True)

    edition_number = _edition_number()

    normalized = []
    for a in articles:
        normalized.append({
            "id": hashlib.sha1(a["url"].encode()).hexdigest()[:12],
            "url": a["url"],
            "source": a["source"],
            "category": a["category"],
            "title_pt": a.get("title_pt", a["title"]),
            "summary_pt": a.get("summary_pt", a.get("summary", ""))[:320],
            "thumbnail": a.get("thumbnail"),
            "score": a.get("score", 5),
            "published_at": a.get("published_at"),
        })

    edition = {
        "date": date,
        "edition_number": edition_number,
        "articles": normalized,
    }

    out_path = EDITIONS_DIR / f"{date}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(edition, f, ensure_ascii=False, indent=2)

    with open(CURRENT_JSON, "w", encoding="utf-8") as f:
        json.dump(edition, f, ensure_ascii=False, indent=2)

    _update_index(date, edition_number, len(normalized))

    print(f"  ✓ Edição salva: {out_path}")
    return edition


def _update_index(date: str, edition_number: int, count: int) -> None:
    index = []
    if EDITIONS_INDEX.exists():
        with open(EDITIONS_INDEX) as f:
            index = json.load(f)

    index = [e for e in index if e["date"] != date]
    index.append({"date": date, "edition_number": edition_number, "count": count})
    index.sort(key=lambda x: x["date"], reverse=True)

    with open(EDITIONS_INDEX, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
