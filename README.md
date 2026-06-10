# Design Week — designteam.com.br

Agregador automático de notícias de design. Roda toda segunda-feira via GitHub Actions.

## Setup rápido

### 1. Clone e configure variáveis

```bash
cp .env.example .env
# edite .env com suas chaves
```

### 2. Instale dependências Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Teste o pipeline localmente

```bash
python main.py
```

Isso vai:
- Coletar ~300 artigos dos 30 feeds RSS
- Deduplificar por URL e similaridade de título
- Traduzir e pontuar com Claude Haiku (sua chave pessoal)
- Salvar top 25 em `data/editions/YYYY-MM-DD.json`
- Gerar newsletter HTML, post LinkedIn e roteiro de podcast em `outputs/`

### 4. Site local

```bash
cd site
npm install
npm run dev   # http://localhost:4321
```

### 5. Deploy no Vercel

1. Crie um repo no GitHub e suba o código
2. Conecte no [vercel.com](https://vercel.com) — detectará o `vercel.json` automaticamente
3. Configure as variáveis de ambiente no painel do Vercel (mesmo que os secrets do GitHub)

### 6. GitHub Actions (automação semanal)

Adicione os secrets no repositório (Settings → Secrets):

| Secret | Valor |
|--------|-------|
| `ANTHROPIC_API_KEY` | sua chave pessoal |
| `RESEND_API_KEY` | chave do Resend (free tier) |
| `RESEND_FROM_EMAIL` | noticias@designteam.com.br |
| `RESEND_AUDIENCE_ID` | ID da lista no Resend (opcional) |

O workflow `.github/workflows/weekly_news.yml` roda toda segunda às 06:00 BRT.

## Custos

| Serviço | Custo |
|---------|-------|
| GitHub Actions | Grátis (público) |
| Vercel | Grátis (hobby plan) |
| Resend | Grátis até 3.000 e-mails/mês |
| Claude Haiku | ~$0.05–0.10 por edição semanal |

## Estrutura

```
collector/      # Feeds RSS + dedup + processamento AI
generators/     # Newsletter, LinkedIn, Podcast, dados do site
site/           # Astro SSG — designteam.com.br
data/           # Edições JSON persistidas (versionadas no git)
outputs/        # HTML, .txt, .md gerados por edição
.github/        # Workflow semanal
```
