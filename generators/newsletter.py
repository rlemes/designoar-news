import resend
from config import RESEND_API_KEY, RESEND_FROM_EMAIL, RESEND_AUDIENCE_ID

CATEGORY_COLORS = {
    "UX Design": "#4A90D9",
    "Design Digital": "#7B61FF",
    "Game Design": "#E85D04",
    "Design de Produto": "#2D6A4F",
    "Arquitetura": "#6B4C3B",
    "Design Gráfico": "#C9184A",
    "Arte & Design": "#6D6875",
}


def generate_newsletter(edition: dict) -> str:
    date_str = edition["date"]
    d, m, y = date_str.split("-")[2], date_str.split("-")[1], date_str.split("-")[0]
    date_br = f"{d}/{m}/{y}"
    n = edition["edition_number"]

    articles_by_cat: dict[str, list] = {}
    for a in edition["articles"]:
        cat = a["category"]
        if cat not in articles_by_cat:
            articles_by_cat[cat] = []
        if len(articles_by_cat[cat]) < 3:
            articles_by_cat[cat].append(a)

    sections_html = ""
    for cat, arts in articles_by_cat.items():
        color = CATEGORY_COLORS.get(cat, "#333")
        cards = ""
        for a in arts:
            thumb = ""
            if a.get("thumbnail"):
                thumb = f'<img src="{a["thumbnail"]}" alt="" style="width:100%;height:180px;object-fit:cover;border-radius:6px 6px 0 0;display:block;">'
            cards += f"""
            <div style="background:#fff;border:1px solid #E5E5E5;border-radius:8px;margin-bottom:16px;overflow:hidden;">
              {thumb}
              <div style="padding:16px;">
                <span style="background:{color};color:#fff;font-size:11px;font-weight:600;padding:3px 8px;border-radius:4px;text-transform:uppercase;letter-spacing:.5px;">{cat}</span>
                <h3 style="font-family:Georgia,serif;font-size:17px;margin:10px 0 6px;color:#1A1A1A;line-height:1.35;">{a["title_pt"]}</h3>
                <p style="font-family:Arial,sans-serif;font-size:14px;color:#555;margin:0 0 12px;line-height:1.5;">{a["summary_pt"]}</p>
                <a href="{a["url"]}" style="color:#2D6A4F;font-size:13px;font-weight:600;text-decoration:none;">{a["source"]} → Ler original</a>
              </div>
            </div>"""

        sections_html += f"""
        <tr><td style="padding:24px 0 8px;">
          <h2 style="font-family:Georgia,serif;font-size:20px;color:#1A1A1A;margin:0;border-bottom:2px solid {color};padding-bottom:8px;">{cat}</h2>
        </td></tr>
        <tr><td>{cards}</td></tr>"""

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Designoar News #{n}</title></head>
<body style="margin:0;padding:0;background:#FAFAF8;font-family:Arial,sans-serif;">
<table width="100%" cellpadding="0" cellspacing="0" style="background:#FAFAF8;">
  <tr><td align="center" style="padding:24px 16px;">
    <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">
      <tr><td style="background:#2D6A4F;padding:32px;border-radius:8px 8px 0 0;text-align:center;">
        <h1 style="font-family:Georgia,serif;color:#fff;font-size:26px;margin:0 0 6px;">Designoar News #{n}</h1>
        <p style="color:rgba(255,255,255,.8);margin:0;font-size:14px;">As melhores notícias de design — {date_br}</p>
      </td></tr>
      <tr><td style="background:#fff;padding:32px;border-radius:0 0 8px 8px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          {sections_html}
          <tr><td style="padding:32px 0 0;text-align:center;border-top:1px solid #E5E5E5;">
            <p style="font-size:13px;color:#888;margin:0;">
              Você recebeu este e-mail por estar inscrito no <a href="https://designteam.com.br" style="color:#2D6A4F;">designteam.com.br</a><br>
              <a href="{{{{unsubscribe}}}}" style="color:#888;">Cancelar inscrição</a>
            </p>
          </td></tr>
        </table>
      </td></tr>
    </table>
  </td></tr>
</table>
</body></html>"""
    return html


def send_newsletter(html: str, edition: dict) -> bool:
    if not RESEND_API_KEY:
        print("  ⚠️  RESEND_API_KEY não configurada — e-mail não enviado")
        return False

    resend.api_key = RESEND_API_KEY
    date_str = edition["date"]
    d, m, y = date_str.split("-")[2], date_str.split("-")[1], date_str.split("-")[0]
    n = edition["edition_number"]
    subject = f"Designoar News #{n} | {d}/{m}/{y} — As melhores notícias de design"

    try:
        params = {
            "from": RESEND_FROM_EMAIL,
            "to": [RESEND_FROM_EMAIL],  # fallback — substitua por audience
            "subject": subject,
            "html": html,
        }
        if RESEND_AUDIENCE_ID:
            params["to"] = [f"audience:{RESEND_AUDIENCE_ID}"]

        resend.Emails.send(params)
        print(f"  ✓ Newsletter enviada: {subject}")
        return True
    except Exception as e:
        print(f"  ⚠️  Erro ao enviar newsletter: {e}")
        return False
