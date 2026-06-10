def generate_linkedin_post(edition: dict) -> str:
    date_str = edition["date"]
    d, m = date_str.split("-")[2], date_str.split("-")[1]
    articles = edition["articles"]

    top = articles[0] if articles else None
    rest = articles[1:5]

    if not top:
        return ""

    lines = [
        f"📐 Design News da Semana — {d}/{m}",
        "",
        "O design nunca para. Esta semana trouxe novidades que todo profissional criativo precisa conhecer.",
        "",
        "🎯 Destaque:",
        f"{top['title_pt']} — {top['summary_pt'][:120]}",
        "",
        "Esta semana também rolou:",
    ]

    for a in rest:
        lines.append(f"• {a['title_pt']}")

    lines += [
        "",
        "Todas as notícias → designteam.com.br",
        "",
        "#Design #UXDesign #DesignNews #DesignBrasil",
    ]

    post = "\n".join(lines)
    return post[:1300]
