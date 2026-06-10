import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
RESEND_API_KEY = os.environ.get("RESEND_API_KEY", "")
RESEND_FROM_EMAIL = os.environ.get("RESEND_FROM_EMAIL", "noticias@designteam.com.br")
RESEND_AUDIENCE_ID = os.environ.get("RESEND_AUDIENCE_ID", "")

CLAUDE_MODEL = "claude-haiku-4-5-20251001"

TOP_ARTICLES = 25
DEDUP_SIMILARITY_THRESHOLD = 0.85
SEEN_URLS_WEEKS = 4
