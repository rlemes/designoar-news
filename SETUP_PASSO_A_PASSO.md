# Designoar News — Setup Completo Passo a Passo

> Guia para quem não tem conhecimento técnico. Cada passo é explicado com prints e sem jargão.

---

## O que você vai precisar (tudo gratuito)

| Conta | Para quê | Link |
|-------|----------|------|
| GitHub | Guardar o código e rodar automaticamente | github.com |
| Vercel | Publicar o site na internet | vercel.com |
| Resend | Enviar e-mail para assinantes | resend.com |
| Anthropic (Claude) | Traduzir e resumir as notícias | console.anthropic.com |

---

## PARTE 1 — Colocar o site no ar (GitHub + Vercel)

### Passo 1: Criar conta no GitHub
1. Acesse **github.com** e clique em "Sign up"
2. Escolha um nome de usuário (ex: `rodrigosoukef`) e crie sua conta
3. Confirme o e-mail que receberá

### Passo 2: Instalar o GitHub Desktop (mais fácil que o terminal)
1. Acesse **desktop.github.com** e baixe o app
2. Instale e faça login com sua conta GitHub
3. Clique em **File → Add local repository**
4. Navegue até a pasta **"Site rss news"** dentro de Documentos
5. Clique em **"Add repository"** → depois **"Publish repository"**
   - Dê o nome: `designoar-news`
   - Deixe marcado **"Keep this code private"** (recomendado)
   - Clique em **Publish repository**
6. ✅ Seu código agora está no GitHub!

### Passo 3: Criar conta no Vercel e conectar ao GitHub
1. Acesse **vercel.com** → clique em "Start Deploying"
2. Escolha **"Continue with GitHub"** e autorize
3. Clique em **"Add New Project"**
4. Encontre **designoar-news** na lista e clique em **"Import"**
5. Na tela de configuração:
   - **Framework Preset**: Other
   - **Build Command**: `cd site && npm install && npm run build`
   - **Output Directory**: `site/dist`
6. Clique em **"Deploy"**
7. Aguarde ~1 minuto → ✅ Seu site está no ar! Você receberá um link como `designoar-news.vercel.app`

---

## PARTE 2 — Configurar as chaves secretas

### Passo 4: Pegar sua chave do Claude (Anthropic)
1. Acesse **console.anthropic.com** → faça login com sua conta
2. No menu lateral, clique em **"API Keys"**
3. Clique em **"Create Key"** → dê o nome "designoar"
4. **COPIE a chave** (começa com `sk-ant-...`) e salve em algum lugar seguro
   > ⚠️ Essa chave aparece só uma vez! Não feche a tela antes de copiar.

### Passo 5: Pegar a chave do Resend (e-mail)
1. Acesse **resend.com** → clique em "Sign Up" (gratuito)
2. Confirme seu e-mail
3. No painel, vá em **"API Keys"** → clique em **"Create API Key"**
4. Nome: "designoar" → clique em **"Add"**
5. Copie a chave (começa com `re_...`)

### Passo 6: Verificar seu domínio de e-mail no Resend
> Isso permite enviar e-mails de noticias@designoar.com.br. Pule este passo se não tiver o domínio ainda — use seu e-mail pessoal por enquanto.

1. No Resend, vá em **"Domains"** → **"Add Domain"**
2. Digite seu domínio e siga as instruções para adicionar registros DNS no seu provedor

### Passo 7: Adicionar as chaves secretas no GitHub
1. Vá até **github.com/SEU_USUARIO/designoar-news**
2. Clique em **Settings** (aba superior direita do repo)
3. No menu lateral, clique em **Secrets and variables → Actions**
4. Clique em **"New repository secret"** e adicione cada um:

| Nome | Valor |
|------|-------|
| `ANTHROPIC_API_KEY` | sua chave do Claude (sk-ant-...) |
| `RESEND_API_KEY` | sua chave do Resend (re_...) |
| `RESEND_FROM_EMAIL` | noticias@designoar.com.br (ou seu e-mail) |

5. ✅ Pronto! O GitHub Actions vai usar essas chaves automaticamente.

---

## PARTE 3 — Testar localmente (opcional mas recomendado)

### Passo 8: Configurar o arquivo .env
1. Na pasta **"Site rss news"**, encontre o arquivo `.env.example`
2. Faça uma cópia e renomeie para `.env` (sem ".example")
3. Abra o `.env` com qualquer editor de texto e preencha:

```
ANTHROPIC_API_KEY=sk-ant-SUA_CHAVE_AQUI
RESEND_API_KEY=re_SUA_CHAVE_AQUI
RESEND_FROM_EMAIL=seu@email.com
```

### Passo 9: Rodar o pipeline pela primeira vez
1. Abra o Terminal (Finder → Aplicativos → Utilitários → Terminal)
2. Digite os comandos abaixo um por um:

```bash
cd "/Users/rosoukef/Documents/Site rss news"
python3 main.py
```

3. Você verá mensagens como:
```
🎨 Designoar News — rodando para 2026-06-10
📡 Coletando feeds RSS...
  ✓ 287 artigos coletados
🔍 Deduplicando...
  ✓ 241 artigos únicos após dedup
🤖 Processando com Claude AI...
  ✓ Processados 10/241 artigos
...
✅ Edição 1 (2026-06-10) concluída — 25 artigos
```

4. Isso vai demorar ~3-5 minutos. Ao final, os arquivos estarão em:
   - `data/editions/2026-06-10.json` — dados da edição
   - `outputs/newsletter_2026-06-10.html` — newsletter pronta
   - `outputs/linkedin_2026-06-10.txt` — post do LinkedIn
   - `outputs/podcast_2026-06-10.md` — roteiro do podcast

### Passo 10: Ver o site com a edição
```bash
cd site
npm run dev
```
Abra **http://localhost:4321** no navegador.

---

## PARTE 4 — Publicar atualização no Vercel

### Passo 11: Enviar os dados gerados para o GitHub
1. Abra o **GitHub Desktop**
2. Você verá os arquivos novos listados (data/, outputs/)
3. Na parte inferior esquerda, escreva uma mensagem como: `"Primeira edição"`
4. Clique em **"Commit to main"**
5. Clique em **"Push origin"** (botão azul no topo)
6. ✅ Em ~1 minuto o Vercel vai redesployar com a nova edição!

---

## PARTE 5 — Automação completa (roda sozinho toda semana)

O arquivo `.github/workflows/weekly_news.yml` já está configurado para rodar **toda segunda-feira às 06:00 (horário de Brasília)**.

**Você não precisa fazer nada!** Toda segunda-feira:
1. O GitHub Actions coleta as notícias
2. Traduz com Claude
3. Gera newsletter, LinkedIn e podcast
4. Commita os dados
5. O Vercel redesployta automaticamente

Para testar manualmente:
1. Vá em **github.com/SEU_USUARIO/designoar-news**
2. Clique em **Actions** (menu superior)
3. Clique em **"Weekly Design News"**
4. Clique em **"Run workflow"** → **"Run workflow"** (botão verde)

---

## PARTE 6 — Domínio personalizado (opcional)

Se você tiver o domínio **designoar.com.br**:

1. No painel do **Vercel**, vá em seu projeto → **Settings → Domains**
2. Clique em **"Add Domain"** e digite `designoar.com.br`
3. O Vercel vai mostrar os registros DNS que você precisa configurar
4. Vá ao seu provedor de domínio (Registro.br, GoDaddy, etc.) e configure os registros
5. Em até 24h o site estará em **designoar.com.br**

---

## Resumo de custos

| Serviço | Plano | Custo |
|---------|-------|-------|
| GitHub | Free | R$ 0 |
| Vercel | Hobby | R$ 0 |
| Resend | Free (3.000 e-mails/mês) | R$ 0 |
| Claude Haiku | Pay per use | ~R$ 0,30 por edição |

**Total por mês: ~R$ 1,20** (4 edições × R$ 0,30)

---

## Problemas comuns

**"python3: command not found"**
→ Instale Python em **python.org/downloads** (baixe a versão 3.11+)

**"ModuleNotFoundError"**
→ Execute: `pip3 install -r requirements.txt`

**Site não atualiza no Vercel**
→ Verifique se o push foi feito no GitHub Desktop. O Vercel só redesployta quando recebe um push.

**Claude retorna erro**
→ Verifique se a `ANTHROPIC_API_KEY` no `.env` está correta e tem créditos disponíveis.
