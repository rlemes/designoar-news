from __future__ import annotations
import requests
from bs4 import BeautifulSoup
import feedparser
from datetime import datetime, timezone


HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; DesignTeamBot/1.0; +https://designteam.com.br)"
}

TIMEOUT = 10


def fetch_article_thumbnail(url: str) -> str | None:
    try:
        resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        soup = BeautifulSoup(resp.text, "lxml")
        tag = soup.find("meta", property="og:image")
        if tag and tag.get("content"):
            return tag["content"]
        tag = soup.find("meta", attrs={"name": "twitter:image"})
        if tag and tag.get("content"):
            return tag["content"]
    except Exception:
        pass
    return None


def fetch_feeds(feeds: list[dict]) -> list[dict]:
    articles = []
    for feed_def in feeds:
        try:
            parsed = feedparser.parse(
                feed_def["url"],
                request_headers={"User-Agent": HEADERS["User-Agent"]},
            )
            for entry in parsed.entries[:15]:
                url = entry.get("link", "")
                if not url:
                    continue

                summary_raw = (
                    entry.get("summary", "")
                    or entry.get("description", "")
                    or ""
                )
                soup = BeautifulSoup(summary_raw, "lxml")
                summary_text = soup.get_text(separator=" ", strip=True)[:500]

                thumbnail = None
                if hasattr(entry, "media_thumbnail") and entry.media_thumbnail:
                    thumbnail = entry.media_thumbnail[0].get("url")
                elif hasattr(entry, "media_content") and entry.media_content:
                    thumbnail = entry.media_content[0].get("url")

                published = None
                if entry.get("published_parsed"):
                    published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).isoformat()
                elif entry.get("updated_parsed"):
                    published = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc).isoformat()

                articles.append({
                    "url": url,
                    "title": entry.get("title", "").strip(),
                    "summary": summary_text,
                    "thumbnail": thumbnail,
                    "source": feed_def["source"],
                    "category": feed_def["category"],
                    "published_at": published,
                })
        except Exception as e:
            print(f"  ⚠️  Feed error ({feed_def['source']}): {e}")
    return articles
