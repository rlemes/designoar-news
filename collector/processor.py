from __future__ import annotations
import json
import anthropic
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL

SYSTEM_PROMPT = """Você é um editor de um agregador de notícias de design brasileiro.
Para cada notícia fornecida, você deve:
1. Traduzir o título para português brasileiro (natural, não literal)
2. Escrever uma chamada de EXATAMENTE até 320 caracteres em português brasileiro.
   Tom: editorial, direto, como uma chamada de revista de design.
   Inclua: o que aconteceu + por que importa para designers.
3. Pontuar a relevância para designers brasileiros de 1-10
4. Confirmar ou corrigir a categoria dentre: UX Design, Design Digital, Game Design, Design de Produto, Arquitetura, Design Gráfico, Arte & Design

Responda APENAS com JSON válido, sem markdown, no formato:
{"title_pt": "...", "summary_pt": "...", "score": 8, "category": "..."}"""


def process_articles(articles: list[dict]) -> list[dict]:
    if not ANTHROPIC_API_KEY:
        print("  ⚠️  ANTHROPIC_API_KEY não configurada — pulando processamento AI")
        for a in articles:
            a["title_pt"] = a["title"]
            a["summary_pt"] = a["summary"][:320]
            a["score"] = 5
        return articles

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    results = []

    for i, article in enumerate(articles):
        try:
            user_content = json.dumps({
                "title": article["title"],
                "summary": article["summary"][:800],
                "category": article["category"],
                "source": article["source"],
            }, ensure_ascii=False)

            msg = client.messages.create(
                model=CLAUDE_MODEL,
                max_tokens=512,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_content}],
            )

            raw = msg.content[0].text.strip()
            if raw.startswith("```"):
                raw = raw.split("\n", 1)[1].rsplit("\n", 1)[0]
            data = json.loads(raw)
            article["title_pt"] = data.get("title_pt", article["title"])
            article["summary_pt"] = data.get("summary_pt", article["summary"])[:320]
            article["score"] = int(data.get("score", 5))
            article["category"] = data.get("category", article["category"])
            results.append(article)

            if (i + 1) % 10 == 0:
                print(f"  ✓ Processados {i + 1}/{len(articles)} artigos")

        except Exception as e:
            print(f"  ⚠️  Erro ao processar '{article['title'][:50]}': {e}")
            article["title_pt"] = article["title"]
            article["summary_pt"] = article["summary"][:320]
            article["score"] = 5
            results.append(article)

    return results
