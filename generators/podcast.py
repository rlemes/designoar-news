def generate_podcast_script(edition: dict) -> str:
    date_str = edition["date"]
    d, m, y = date_str.split("-")[2], date_str.split("-")[1], date_str.split("-")[0]
    articles = edition["articles"]
    n = edition["edition_number"]

    top = articles[0] if articles else None

    by_cat: dict[str, list] = {}
    for a in articles[1:]:
        cat = a["category"]
        if cat not in by_cat:
            by_cat[cat] = []
        by_cat[cat].append(a)

    def cat_block(cat: str, duration: str) -> str:
        arts = by_cat.get(cat, [])[:3]
        if not arts:
            return ""
        lines = [f"\n## [{cat.upper()} — {duration}]\n"]
        for a in arts:
            lines.append(f"**{a['title_pt']}** ({a['source']})")
            lines.append(f"{a['summary_pt']}")
            lines.append("[RESPIRA]\n")
        lines.append("[TRANSIÇÃO]\n")
        return "\n".join(lines)

    script = f"""# Designoar News #{n} — Roteiro do Podcast
**Data:** {d}/{m}/{y}
**Duração estimada:** 30 minutos

---

## [INTRO — 2min]

Olá, olá! Bem-vindo ao Designoar News, o podcast semanal da designteam.com.br — seu resumo do que aconteceu no mundo do design nesta semana.

Eu sou seu host, e hoje é {d} de {"janeiro,fevereiro,março,abril,maio,junho,julho,agosto,setembro,outubro,novembro,dezembro".split(",")[int(m)-1]} de {y}.

Vamos direto ao que importa: as notícias mais relevantes de design para você, profissional criativo.

[RESPIRA]

---

## [DESTAQUE DA SEMANA — 5min]
"""

    if top:
        script += f"""
**Notícia:** {top["title_pt"]}
**Fonte:** {top["source"]} | **Categoria:** {top["category"]}

{top["summary_pt"]}

[ÊNFASE]

E por que isso importa para você, designer? Porque mostra como o campo continua evoluindo — e quem não acompanha, fica pra trás.

[PAUSA]

---
"""

    script += cat_block("UX Design", "5min")
    script += cat_block("Design Digital", "4min")
    script += cat_block("Design de Produto", "4min")
    script += cat_block("Design Gráfico", "3min")
    script += cat_block("Game Design", "3min")
    script += cat_block("Arquitetura", "2min")
    script += cat_block("Arte & Design", "2min")

    script += """
## [ENCERRAMENTO — 2min]

É isso por hoje, galera! Essas foram as principais notícias de design desta semana.

Se você curtiu, compartilha com aquele colega designer que você conhece — e não esqueça de acessar **designteam.com.br** para ler todas as notícias com mais detalhe.

Nos vemos semana que vem. Até lá!

[FIM]
"""
    return script
