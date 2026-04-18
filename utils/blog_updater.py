import os
import sys
import requests
import google.generativeai as genai
from slugify import slugify
from datetime import datetime

# Keys read from GitHub Secrets (injected as environment variables)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Resolve the project root regardless of where the script is called from
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR = os.path.join(PROJECT_ROOT, 'data', 'blog_posts')


def validate_env():
    """Abort early if required environment variables are missing."""
    missing = [k for k in ('NEWS_API_KEY', 'GEMINI_API_KEY') if not os.getenv(k)]
    if missing:
        print(f"[ERROR] Missing environment variables: {', '.join(missing)}")
        sys.exit(1)


def get_tech_news() -> list[dict]:
    """Fetch the 5 most recent English articles about AI / Data Science."""
    url = (
        'https://newsapi.org/v2/everything'
        '?q=AI+OR+"Artificial+Intelligence"+OR+Python+OR+"Data+Science"'
        '&language=en'
        '&sortBy=publishedAt'
        '&pageSize=5'
        f'&apiKey={NEWS_API_KEY}'
    )
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json().get('articles', [])
    except requests.RequestException as e:
        print(f"[ERROR] Failed to fetch news: {e}")
        return []


def summarize_with_gemini(title: str, description: str, source_url: str) -> str:
    """Generate a professional Portuguese summary using Gemini 1.5 Flash."""
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')  # gemini-pro is deprecated

    prompt = f"""
Aja como um especialista em tecnologia e Ciência de Dados escrevendo para um blog de portfólio profissional.

Escreva um artigo completo em Português do Brasil sobre a notícia abaixo.
Formate tudo em Markdown. Estruture assim:

1. Um parágrafo de introdução contextualizado
2. Os pontos principais da notícia (em tópicos)
3. Uma seção "## Minha Análise" explicando por que isso é relevante para desenvolvedores Python ou Cientistas de Dados

Título Original: {title}
Descrição: {description}
URL da fonte: {source_url}

Responda apenas com o corpo do artigo em Markdown, sem título (o título já está no front matter).
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"[WARNING] Gemini failed, using fallback content. Error: {e}")
        return f"{description}\n\n[Leia o artigo completo aqui]({source_url})"


def escape_yaml_string(text: str) -> str:
    """Escape double quotes inside YAML front matter string values."""
    return text.replace('"', '\\"') if text else ''


def build_post_content(article: dict, body: str) -> str:
    """Assemble the full Markdown file with YAML front matter."""
    title = escape_yaml_string(article['title'])
    description = article.get('description') or ''
    summary_excerpt = escape_yaml_string(description[:150])
    image = article.get('urlToImage') or 'https://placehold.co/800x400?text=Tech+News'
    source_url = article['url']
    today = datetime.now().strftime('%Y-%m-%d')

    return f"""---
title: "{title}"
date: {today}
summary: "{summary_excerpt}..."
image: {image}
tags: [AI, Data Science, Tech News]
---

{body}

---
*Fonte original: [{article['title']}]({source_url})*
"""


def update_blog():
    validate_env()
    os.makedirs(BLOG_DIR, exist_ok=True)

    articles = get_tech_news()
    if not articles:
        print("[INFO] No articles returned. Exiting.")
        return

    for article in articles:
        title = article.get('title', '')

        # Skip removed or empty articles
        if not title or '[Removed]' in title:
            continue

        slug = slugify(title)
        filepath = os.path.join(BLOG_DIR, f'{slug}.md')

        # Skip duplicates
        if os.path.exists(filepath):
            print(f"[SKIP] Already exists: {slug}")
            continue

        description = article.get('description') or 'No description available.'
        print(f"[INFO] Processing: {title}")

        body = summarize_with_gemini(title, description, article['url'])
        content = build_post_content(article, body)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"[OK] Saved: {filepath}")
        break  # One post per run — keeps the blog fresh daily


if __name__ == '__main__':
    update_blog()
