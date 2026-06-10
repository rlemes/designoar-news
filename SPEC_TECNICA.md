# Designoar News — Spec Técnica Completa
> Documento de handoff para continuidade no VSCode com Claude

---

## 1. Visão Geral do Projeto

**Designoar News** é um agregador automático de notícias de design para o público brasileiro.

Um pipeline Python roda toda segunda-feira às 06h (horário de Brasília) via GitHub Actions:
1. Coleta artigos de ~30 feeds RSS de design
2. Remove duplicatas por URL e similaridade de título (TF-IDF)
3. Traduz títulos e resume em PT-BR via Claude Haiku (Anthropic API)
4. Gera 4 outputs: site estático, newsletter HTML, post LinkedIn, roteiro de podcast

**Domínio:** designteam.com.br (Vercel)
**Idioma dos outputs:** Português Brasileiro
**Custo estimado:** ~R$ 0,30/semana (só a API do Claude Haiku)

---

## 2. Estado Atual — O que já está pronto

| Módulo | Status | Observação |
|--------|--------|------------|
| `collector/feeds.py` | ✅ Completo | 30 feeds, 7 categorias |
| `collector/scraper.py` | ✅ Completo | feedparser + extração og:image |
| `collector/dedup.py` | ✅ Completo | URL normalize + TF-IDF cosine |
| `collector/processor.py` | ✅ Completo | Claude Haiku — traduz, resume, pontua |
| `generators/site_data.py` | ✅ Completo | Gera JSON da edição + índice |
| `generators/newsletter.py` | ✅ Completo | HTML responsivo + envio via Resend |
| `generators/linkedin.py` | ✅ Completo | Post PT-BR, max 1300 chars |
| `generators/podcast.py` | ✅ Completo | Roteiro .md com marcadores de locução |
| `main.py` | ✅ Completo | Orquestração completa do pipeline |
| `site/` Astro — layout | ✅ Completo | Base.astro com header/footer |
| `site/` Astro — componentes | ✅ Completo | NewsCard, CategoryTag, EditionNav |
| `site/` Astro — páginas | ✅ Completo | index, /edicoes/, /edicoes/[slug] |
| `.github/workflows/` | ✅ Completo | Cron toda segunda, 09:00 UTC |
| `vercel.json` | ✅ Completo | Build config para Vercel |
| **Primeira edição** | ✅ Gerada | `data/editions/2026-06-10.json` — 25 artigos |

### Pendências conhecidas
- [ ] Thumbnails da edição atual estão `null` — o enriquecimento de og:image foi pulado na primeira run (sem chave Anthropic válida no momento)
- [ ] Títulos e resumos estão em inglês (sem tradução) — mesma razão acima
- [ ] Precisa subir para GitHub + Vercel + configurar DNS do designteam.com.br
- [ ] Validar envio de newsletter via Resend quando chave for configurada
- [ ] Melhorar o design da newsletter HTML para ficar consistente com o site

---

## 3. Stack Técnica

```
Python 3.9+          Pipeline de coleta e geração
  feedparser         Parsing de RSS
  beautifulsoup4     Extração de og:image
  scikit-learn       TF-IDF para dedup
  anthropic          Claude Haiku — tradução e scoring
  resend             Envio de newsletter
  python-dotenv      Variáveis de ambiente

Astro 6.3.x          Site estático (SSG)
  Node 22+
  TypeScript

GitHub Actions       Automação semanal (cron)
Vercel               Hosting + deploy automático
```

---

## 4. Estrutura de Arquivos

```
designteam-news/                    ← raiz do projeto
├── .env                            ← chaves secretas (não commitar)
├── .env.example                    ← template das variáveis
├── .gitignore
├── .github/
│   └── workflows/
│       └── weekly_news.yml         ← cron GitHub Actions
├── collector/
│   ├── feeds.py                    ← lista estática de 30 feeds RSS
│   ├── scraper.py                  ← fetch + extração og:image
│   ├── dedup.py                    ← deduplicação URL + TF-IDF
│   └── processor.py                ← Claude API: traduz, resume, pontua
├── generators/
│   ├── site_data.py                ← gera JSON da edição + índice
│   ├── newsletter.py               ← HTML email + envio Resend
│   ├── linkedin.py                 ← post texto LinkedIn
│   └── podcast.py                  ← roteiro .md para podcast
├── config.py                       ← lê variáveis do .env
├── main.py                         ← orquestrador principal
├── requirements.txt
├── vercel.json                     ← config de deploy
├── data/
│   ├── seen_urls.json              ← URLs já publicadas (últimas 4 semanas)
│   └── editions/
│       └── YYYY-MM-DD.json         ← uma edição por semana
├── outputs/                        ← gerados a cada run (não commitar)
│   ├── newsletter_YYYY-MM-DD.html
│   ├── linkedin_YYYY-MM-DD.txt
│   └── podcast_YYYY-MM-DD.md
└── site/                           ← projeto Astro
    ├── astro.config.mjs
    ├── package.json
    ├── vercel.json
    └── src/
        ├── layouts/
        │   └── Base.astro          ← header/footer global
        ├── components/
        │   ├── NewsCard.astro      ← card de artigo (normal + featured)
        │   ├── CategoryTag.astro   ← tag colorida de categoria
        │   └── EditionNav.astro    ← navegação entre edições
        ├── pages/
        │   ├── index.astro         ← edição atual
        │   ├── edicoes/
        │   │   ├── index.astro     ← arquivo de todas as edições
        │   │   └── [slug].astro    ← edição individual (slug = YYYY-MM-DD)
        └── data/
            ├── current.json        ← edição mais recente (copiada pelo pipeline)
            └── editions_index.json ← lista de todas as edições
```

---

## 5. Design System

Referência visual: **dezeen.com** — editorial, clean, tipografia forte, muito espaço em branco.

### Fontes
```
DM Serif Display  →  títulos, headlines, nome do veículo
DM Sans           →  corpo de texto, labels, meta
```
Carregadas via Google Fonts no `Base.astro`.

### Paleta
```css
--white:     #ffffff   /* fundo principal */
--black:     #0a0a0a   /* texto, bordas fortes */
--gray-100:  #f7f7f7   /* fundo hover suave */
--gray-200:  #ebebeb   /* bordas divisórias */
--gray-400:  #999999   /* textos secundários, datas */
--gray-600:  #555555   /* texto de apoio */
--accent:    #c8001e   /* vermelho editorial — badges, hover, destaque */
```

### Tags de Categoria (outline colorido, sem fundo)
```
UX Design         #1a6fb5  (azul)
Design Digital    #5b3faa  (roxo)
Game Design       #c8001e  (vermelho)
Design de Produto #0d7045  (verde escuro)
Arquitetura       #7a4526  (marrom)
Design Gráfico    #c8001e  (vermelho)
Arte & Design     #444444  (cinza escuro)
```

### Componentes-chave

**Header** — sticky, borda inferior `2px solid #0a0a0a`, logo com ponto vermelho, nav uppercase.

**NewsCard** — dois modos:
- `featured={true}` → layout horizontal full-width, imagem 55%, título 32px+
- padrão → coluna, borda superior 2px que vira `--accent` no hover, imagem 16:9

**Grid de artigos**
```
Desktop (>1024px):  3 colunas, gap 40px
Tablet (768-1024px): 2 colunas
Mobile (<640px):    1 coluna
```

**Separador de seção por categoria**
```css
/* linha cinza que preenche o espaço após o label */
.cat-heading::after { content:''; flex:1; height:1px; background:#ebebeb; }
```

### Estrutura de página (index.astro)
```
[HEADER sticky]
[ISSUE HEADER]  — badge vermelho + título serif grande + data
[FEATURED]      — primeiro artigo em destaque (NewsCard featured)
[por categoria] — heading uppercase + grid de cards
[EDITION NAV]   — ← anterior | arquivo | seguinte →
[FOOTER]
```

---

## 6. Schema de Dados

### Edição (data/editions/YYYY-MM-DD.json)
```json
{
  "date": "2026-06-10",
  "edition_number": 1,
  "articles": [
    {
      "id": "sha1_url[:12]",
      "url": "https://...",
      "source": "UX Collective",
      "category": "UX Design",
      "title_pt": "Título em português",
      "summary_pt": "Resumo em PT-BR, máximo 320 caracteres.",
      "thumbnail": "https://imagem-og.jpg",
      "score": 8,
      "published_at": "2026-06-09T23:00:00+00:00"
    }
  ]
}
```

### Índice de edições (site/src/data/editions_index.json)
```json
[
  { "date": "2026-06-10", "edition_number": 1, "count": 25 }
]
```

### Variáveis de ambiente (.env)
```
ANTHROPIC_API_KEY=sk-ant-...     ← obrigatório para tradução
RESEND_API_KEY=re_...             ← para envio de newsletter
RESEND_FROM_EMAIL=noticias@designteam.com.br
RESEND_AUDIENCE_ID=               ← ID da lista de assinantes no Resend
```

---

## 7. Pipeline Python — Fluxo Completo

```
main.py
  │
  ├─ fetch_feeds(FEEDS)                   ← scraper.py — feedparser dos 30 feeds
  │    └─ retorna: [{url, title, summary, thumbnail, source, category, published_at}]
  │
  ├─ deduplicate(articles, seen_urls)     ← dedup.py
  │    ├─ remove URLs normalizadas já vistas (últimas 4 semanas)
  │    └─ remove títulos similares no batch (TF-IDF cosine ≥ 0.85)
  │
  ├─ process_articles(articles)           ← processor.py — Claude Haiku
  │    └─ adiciona: title_pt, summary_pt (≤320 chars), score (1-10), category
  │
  ├─ sorted by score, top 25
  │
  ├─ enrich_thumbnails()                  ← scraper.py — busca og:image para artigos sem thumb
  │
  ├─ save_seen_urls()                     ← persiste URLs em data/seen_urls.json
  │
  ├─ generate_edition()                   ← site_data.py — salva JSON + atualiza índice
  ├─ generate_newsletter()                ← newsletter.py — HTML responsivo
  ├─ generate_linkedin_post()             ← linkedin.py
  ├─ generate_podcast_script()            ← podcast.py
  │
  ├─ save_outputs()                       ← salva em outputs/
  └─ send_newsletter()                    ← envia via Resend API
```

### Prompt do Claude (processor.py)
```
System: Você é um editor de um agregador de notícias de design brasileiro.
Para cada notícia, responda APENAS com JSON válido:
{
  "title_pt": "título em PT-BR natural",
  "summary_pt": "até 320 chars, tom editorial, o que aconteceu + por que importa",
  "score": 8,          ← relevância para designers brasileiros 1-10
  "category": "..."    ← uma das 7 categorias válidas
}

Categorias válidas: UX Design, Design Digital, Game Design,
Design de Produto, Arquitetura, Design Gráfico, Arte & Design
```
Modelo: `claude-haiku-4-5-20251001` — custo ~$0.001 por artigo.

---

## 8. Feeds RSS Configurados

```python
# collector/feeds.py — 30 feeds, 7 categorias

UX Design (5):
  uxdesign.cc/feed, feeds.feedburner.com/nngroup,
  smashingmagazine.com/feed/, uxplanet.org/feed, alistapart.com/rss.xml

Design Digital (5):
  dribbble.com/stories/recent.rss, tympanus.net/codrops/feed/,
  designmodo.com/feed/, creativebloq.com/feeds/all, awwwards.com/blog/rss/

Game Design (3):
  gamedeveloper.com/rss.xml, 80.lv/feed/, polygon.com/rss/index.xml

Design de Produto (5):
  core77.com/rss.xml, yankodesign.com/feed/, design-milk.com/feed/,
  dezeen.com/feed/, fastcompany.com/design/rss

Arquitetura (4):
  archdaily.com.br/br/feed, dezeen.com/architecture/feed/,
  archinect.com/news/rss.php, wallpaper.com/rss

Design Gráfico (4):
  itsnicethat.com/rss, designweek.co.uk/feed/,
  creativeboom.com/feed/, underconsideration.com/brandnew/feed.rss

Arte & Design (4):
  artsy.net/rss/news, hyperallergic.com/feed/,
  theartnewspaper.com/rss, designboom.com/feed/
```

---

## 9. GitHub Actions

```yaml
# .github/workflows/weekly_news.yml
on:
  schedule:
    - cron: '0 9 * * 1'   # Segunda, 09:00 UTC = 06:00 BRT
  workflow_dispatch:        # disparo manual para testes

jobs:
  collect-and-publish:
    runs-on: ubuntu-latest
    permissions:
      contents: write       # necessário para git push
    steps:
      - actions/checkout@v4
      - actions/setup-python@v5 (3.11)
      - pip install -r requirements.txt
      - python main.py        ← com secrets como env vars
      - git add data/ site/src/data/ outputs/
      - git commit + push     ← trigger automático no Vercel
```

### Secrets necessários no GitHub
```
ANTHROPIC_API_KEY   obrigatório
RESEND_API_KEY      para newsletter (opcional por enquanto)
RESEND_FROM_EMAIL   noticias@designteam.com.br
RESEND_AUDIENCE_ID  ID da audiência no Resend (opcional)
```

---

## 10. Deploy — Vercel

```json
// vercel.json (na raiz)
{
  "buildCommand": "cd site && npm install && npm run build",
  "outputDirectory": "site/dist",
  "framework": null,
  "installCommand": "cd site && npm install"
}
```

Fluxo de deploy:
```
git push (GitHub Actions) → Vercel detecta → build → live em designteam.com.br
```

---

## 11. Tarefas Pendentes — Próximos Passos

### Prioridade Alta
1. **Re-rodar o pipeline com chave válida** — a primeira edição (`2026-06-10`) foi gerada sem tradução (chave expirada). Rodar novamente para ter títulos em PT-BR e scores reais.
   ```bash
   # apagar edição atual, limpar seen_urls e re-rodar
   rm data/editions/2026-06-10.json
   echo "{}" > data/seen_urls.json
   python3 main.py
   ```

2. **Subir para GitHub** — via GitHub Desktop:
   - Criar repo `designteam-news`
   - Publish repository
   - Adicionar secrets: `ANTHROPIC_API_KEY`

3. **Deploy no Vercel** — conectar ao repo GitHub, configurar build command

4. **DNS** — apontar `designteam.com.br` para Vercel (registro A + CNAME)

### Prioridade Média
5. **Newsletter HTML** — atualizar estilo para ficar alinhado com o design do site (atualmente usa o design antigo verde musgo, não o novo preto/vermelho editorial)

6. **Página 404** — criar `site/src/pages/404.astro`

7. **Favicon** — substituir o favicon padrão do Astro pelo logo Designoar News

8. **OG tags** — adicionar `og:image`, `og:title`, `og:description` no `Base.astro` para compartilhamento no LinkedIn/WhatsApp

### Prioridade Baixa
9. **Página de assinatura da newsletter** — form simples com Resend para coletar assinantes

10. **Feed RSS do próprio site** — `/rss.xml` com as edições publicadas

11. **Busca** — campo de busca nas edições anteriores

---

## 12. Como Rodar Localmente

```bash
# Na raiz do projeto
cd "/Users/rosoukef/Documents/Site rss news"

# Rodar pipeline completo (precisa de ANTHROPIC_API_KEY no .env)
python3 main.py

# Ver o site (em outro terminal, após rodar o pipeline)
cd site
npm run dev
# → abre em http://localhost:4321
```

---

## 13. Problemas Conhecidos

| Problema | Causa | Solução |
|----------|-------|---------|
| Python 3.9 no Mac — `str \| None` dá erro | Sintaxe union foi introduzida no 3.10 | Todos os arquivos já têm `from __future__ import annotations` no topo |
| npm install falha sem `--registry` | npm local aponta para registry privado | Usar `npm install --registry https://registry.npmjs.org` na primeira vez |
| `seen_urls.json` vazio na segunda run | Normal — foi commitado vazio | Após a primeira run real, o arquivo é atualizado automaticamente |
| Thumbnails null na edição atual | Pipeline rodou sem a API key | Re-rodar após configurar chave válida |

---

## 14. Prompt para o Claude no VSCode

Cole este prompt para o Claude continuar o projeto a partir deste ponto:

```
Você está assumindo o desenvolvimento do projeto Designoar News.
O projeto já existe e está funcional. Leia o arquivo SPEC_TECNICA.md
na raiz do projeto antes de qualquer coisa — ele descreve tudo:
estrutura, estado atual, pendências e decisões de design.

Pasta do projeto: /Users/rosoukef/Documents/Site rss news

Antes de qualquer tarefa, execute:
  cat "/Users/rosoukef/Documents/Site rss news/SPEC_TECNICA.md"

Em seguida, pergunte qual das tarefas da seção "11. Tarefas Pendentes"
o usuário quer resolver primeiro, e execute passo a passo,
verificando o resultado de cada passo antes de continuar.

Regras:
- Sempre rodar o build do Astro após editar arquivos .astro:
    cd site && npm run build
- Nunca commitar o arquivo .env
- Preservar o design system descrito na seção 5
- Código Python deve ter `from __future__ import annotations` no topo
  (compatibilidade com Python 3.9)
```
```

---

*Spec v2.0 — Junho 2026 — Estado atual: pipeline funcional, site buildando, primeira edição gerada*
