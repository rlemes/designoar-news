#!/usr/bin/env python3
"""Orchestrator — Designoar News pipeline."""
import json
from datetime import datetime, timezone
from pathlib import Path

from collector.feeds import FEEDS
from collector.scraper import fetch_feeds, fetch_article_thumbnail
from collector.dedup import load_seen_urls, save_seen_urls, deduplicate
from collector.processor import process_articles
from generators.site_data import generate_edition
from generators.newsletter import generate_newsletter, send_newsletter
from generators.linkedin import generate_linkedin_post
from generators.podcast import generate_podcast_script
from config import TOP_ARTICLES


def today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def save_outputs(newsletter_html: str, linkedin_txt: str, podcast_md: str, date: str) -> None:
    out = Path("outputs")
    out.mkdir(exist_ok=True)
    (out / f"newsletter_{date}.html").write_text(newsletter_html, encoding="utf-8")
    (out / f"linkedin_{date}.txt").write_text(linkedin_txt, encoding="utf-8")
    (out / f"podcast_{date}.md").write_text(podcast_md, encoding="utf-8")
    print(f"  ✓ Outputs salvos em outputs/")


def enrich_thumbnails(articles: list[dict]) -> list[dict]:
    for a in articles:
        if not a.get("thumbnail"):
            a["thumbnail"] = fetch_article_thumbnail(a["url"])
    return articles


def main():
    date = today()
    print(f"\n🎨 Designoar News — rodando para {date}\n")

    # 1. Collect
    print("📡 Coletando feeds RSS...")
    articles = fetch_feeds(FEEDS)
    print(f"  ✓ {len(articles)} artigos coletados")

    # 2. Dedup
    print("🔍 Deduplicando...")
    seen = load_seen_urls()
    articles = deduplicate(articles, seen)
    print(f"  ✓ {len(articles)} artigos únicos após dedup")

    if not articles:
        print("⚠️  Nenhum artigo novo esta semana. Abortando.")
        return

    # 3. Process with AI
    print("🤖 Processando com Claude AI...")
    articles = process_articles(articles)

    # 4. Select top N
    articles = sorted(articles, key=lambda x: x.get("score", 5), reverse=True)[:TOP_ARTICLES]
    print(f"  ✓ Top {len(articles)} artigos selecionados")

    # 5. Enrich thumbnails
    print("🖼️  Buscando thumbnails...")
    articles = enrich_thumbnails(articles)

    # 6. Update seen URLs
    now_iso = datetime.now(timezone.utc).isoformat()
    for a in articles:
        seen[a.get("_norm_url", a["url"])] = now_iso
    save_seen_urls(seen)

    # 7. Generate outputs
    print("📝 Gerando conteúdo...")
    edition = generate_edition(articles, date)
    newsletter_html = generate_newsletter(edition)
    linkedin_txt = generate_linkedin_post(edition)
    podcast_md = generate_podcast_script(edition)

    # 8. Save outputs
    save_outputs(newsletter_html, linkedin_txt, podcast_md, date)

    # 9. Send newsletter
    print("📧 Enviando newsletter...")
    send_newsletter(newsletter_html, edition)

    print(f"\n✅ Edição {edition['edition_number']} ({date}) concluída — {len(articles)} artigos\n")


if __name__ == "__main__":
    main()
