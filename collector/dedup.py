from __future__ import annotations
import json
import hashlib
from pathlib import Path
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse, urlunparse

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from config import DEDUP_SIMILARITY_THRESHOLD

SEEN_URLS_PATH = Path("data/seen_urls.json")


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    normalized = parsed._replace(
        scheme=parsed.scheme.lower(),
        netloc=parsed.netloc.lower(),
        fragment="",
        query="",
    )
    path = normalized.path.rstrip("/")
    return urlunparse(normalized._replace(path=path))


def load_seen_urls() -> dict:
    if not SEEN_URLS_PATH.exists():
        return {}
    with open(SEEN_URLS_PATH) as f:
        return json.load(f)


def save_seen_urls(seen: dict) -> None:
    SEEN_URLS_PATH.parent.mkdir(parents=True, exist_ok=True)
    cutoff = (datetime.now(timezone.utc) - timedelta(weeks=4)).isoformat()
    pruned = {url: ts for url, ts in seen.items() if ts > cutoff}
    with open(SEEN_URLS_PATH, "w") as f:
        json.dump(pruned, f, indent=2)


def deduplicate(articles: list[dict], seen: dict) -> list[dict]:
    now = datetime.now(timezone.utc).isoformat()

    # 1. Remove URLs already seen in past 4 weeks
    fresh = []
    for a in articles:
        norm = _normalize_url(a["url"])
        if norm not in seen:
            a["_norm_url"] = norm
            fresh.append(a)

    if not fresh:
        return []

    # 2. TF-IDF dedup within current batch
    titles = [a["title"] for a in fresh]
    if len(titles) < 2:
        return fresh

    vec = TfidfVectorizer(stop_words="english").fit_transform(titles)
    sim = cosine_similarity(vec)

    keep = []
    dropped = set()
    for i, article in enumerate(fresh):
        if i in dropped:
            continue
        keep.append(article)
        for j in range(i + 1, len(fresh)):
            if sim[i, j] >= DEDUP_SIMILARITY_THRESHOLD:
                dropped.add(j)

    return keep


def article_id(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:12]
