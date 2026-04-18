"""
blog_updater.py
---------------
Daily automation: fetch a tech news article, extract its full text with
newspaper3k, then use Gemini to write a short English summary + dev analysis.
Saves the result as a Markdown file ready for the Flask blog.
Also writes a LinkedIn-ready .txt draft alongside the blog post.
"""

import os
import sys
import requests
from google import genai
from slugify import slugify
from datetime import datetime

try:
    from newspaper import Article
    NEWSPAPER_AVAILABLE = True
except ImportError:
    NEWSPAPER_AVAILABLE = False
    print("[WARNING] newspaper3k not installed; falling back to API description.")

NEWS_API_KEY   = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR     = os.path.join(PROJECT_ROOT, 'data', 'blog_posts')
LINKEDIN_DIR = os.path.join(PROJECT_ROOT, 'data', 'linkedin_drafts')


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_env():
    missing = [k for k in ('NEWS_API_KEY', 'GEMINI_API_KEY') if not os.getenv(k)]
    if missing:
        print(f"[ERROR] Missing environment variables: {', '.join(missing)}")
        sys.exit(1)


# ---------------------------------------------------------------------------
# News fetching
# ---------------------------------------------------------------------------

def get_tech_news() -> list[dict]:
    """Return up to 10 recent English articles on AI / Python / Data Science."""
    url = (
        'https://newsapi.org/v2/everything'
        '?q=AI+OR+"machine+learning"+OR+Python+OR+"data+science"'
        '&language=en'
        '&sortBy=publishedAt'
        '&pageSize=10'
        f'&apiKey={NEWS_API_KEY}'
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json().get('articles', [])
    except requests.RequestException as e:
        print(f"[ERROR] NewsAPI request failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Full-text extraction
# ---------------------------------------------------------------------------

def extract_full_text(url: str) -> str:
    """
    Use newspaper3k to download and parse the article body.
    Returns an empty string on any failure so callers can fall back gracefully.
    """
    if not NEWSPAPER_AVAILABLE:
        return ''
    try:
        article = Article(url)
        article.download()
        article.parse()
        text = article.text.strip()
        # Very short results are usually boilerplate — treat as failure
        return text if len(text) > 200 else ''
    except Exception as e:
        print(f"[WARNING] newspaper3k failed for {url}: {e}")
        return ''


# ---------------------------------------------------------------------------
# Gemini generation
# ---------------------------------------------------------------------------

def generate_with_gemini(title: str, body_text: str, source_url: str) -> dict:
    """
    Given the article title and body, ask Gemini to produce:
      - blog_post : a structured Markdown article (in English)
      - linkedin  : a short, punchy LinkedIn post (in English)

    Returns a dict with keys 'blog_post' and 'linkedin'.
    Falls back to plain text on any API error.
    """
    client  = genai.Client(api_key=GEMINI_API_KEY)
    excerpt = body_text[:3000] if body_text else "(no full text available)"

    prompt = f"""
You are a senior Data Scientist and Python developer writing for a professional portfolio blog.

Below is an article you have read. Your job is to write TWO pieces of content.

---
ARTICLE TITLE: {title}
ARTICLE BODY (excerpt):
{excerpt}
SOURCE URL: {source_url}
---

OUTPUT FORMAT — respond with exactly this structure (no extra text outside the markers):

===BLOG_START===
[Write a complete Markdown blog post IN ENGLISH with this structure:
1. A short contextual introduction (2-3 sentences) in your own words
2. ## Key Takeaways — bullet points of the most important facts
3. ## Why This Matters for Devs & Data Scientists — your genuine analysis:
   what tools, libraries, or workflows does this affect? what should practitioners do next?
Keep the total length between 300-500 words. Do NOT include a title heading.]
===BLOG_END===

===LINKEDIN_START===
[Write a punchy LinkedIn post IN ENGLISH, max 5 sentences:
- Hook sentence that makes a developer stop scrolling
- 2-3 sentences of insight (your take, not a summary)
- A closing question or call-to-action to drive comments
- 3-5 relevant hashtags: #Python #DataScience #MachineLearning #AI #Dev
Do NOT include any URL — it will be appended automatically.]
===LINKEDIN_END===
"""

    try:
        response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        raw       = response.text
        blog_post = _extract_between(raw, '===BLOG_START===', '===BLOG_END===')
        linkedin  = _extract_between(raw, '===LINKEDIN_START===', '===LINKEDIN_END===')

        if not blog_post:
            raise ValueError("Gemini response missing BLOG block")

        return {'blog_post': blog_post.strip(), 'linkedin': linkedin.strip()}

    except Exception as e:
        print(f"[WARNING] Gemini failed: {e}")
        fallback_body = (
            f"{body_text[:400] or 'No content extracted.'}\n\n"
            f"[Read the full article here]({source_url})"
        )
        fallback_li = (
            f"Interesting read: {title}\n\n"
            "#Python #DataScience #AI"
        )
        return {'blog_post': fallback_body, 'linkedin': fallback_li}


def _extract_between(text: str, start: str, end: str) -> str:
    try:
        return text.split(start)[1].split(end)[0]
    except IndexError:
        return ''


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def escape_yaml(text: str) -> str:
    return text.replace('"', '\\"') if text else ''


def write_blog_post(article: dict, blog_body: str) -> tuple[str, str]:
    """Write the .md file. Returns (filepath, slug)."""
    os.makedirs(BLOG_DIR, exist_ok=True)
    slug     = slugify(article['title'])
    filepath = os.path.join(BLOG_DIR, f'{slug}.md')
    title    = escape_yaml(article['title'])
    desc     = escape_yaml((article.get('description') or '')[:150])
    image    = article.get('urlToImage') or 'https://placehold.co/800x400?text=Tech+News'
    today    = datetime.now().strftime('%Y-%m-%d')
    source   = article['url']

    content = f"""---
title: "{title}"
date: {today}
summary: "{desc}..."
image: {image}
tags: [AI, Data Science, Python, Tech News]
---

{blog_body}

---
*Original source: [{article['title']}]({source})*
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath, slug


def write_linkedin_draft(article: dict, linkedin_text: str, blog_slug: str) -> str:
    """
    Write a ready-to-paste LinkedIn post as a .txt file.
    Replace YOUR_DOMAIN with your actual Railway URL.
    """
    os.makedirs(LINKEDIN_DIR, exist_ok=True)
    slug     = slugify(article['title'])
    filepath = os.path.join(LINKEDIN_DIR, f'{slug}.txt')
    today    = datetime.now().strftime('%Y-%m-%d')

    # ⚠️  Replace with your actual Railway domain
    blog_url = f"https://www.wolflergf.com/blog/{blog_slug}"

    content = (
        f"# LinkedIn Draft — {today}\n"
        f"# Copy everything below this line and paste into LinkedIn.\n"
        f"# Update the blog URL if needed: {blog_url}\n"
        f"# {'─' * 60}\n\n"
        f"{linkedin_text}\n\n"
        f"Read my full take 👉 {blog_url}\n"
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def update_blog():
    validate_env()

    articles = get_tech_news()
    if not articles:
        print("[INFO] No articles returned. Exiting.")
        return

    for article in articles:
        title = article.get('title', '')
        if not title or '[Removed]' in title:
            continue

        slug     = slugify(title)
        filepath = os.path.join(BLOG_DIR, f'{slug}.md')

        if os.path.exists(filepath):
            print(f"[SKIP] Already exists: {slug}")
            continue

        print(f"[INFO] Processing: {title}")

        # Step 1 — try to extract full article text
        full_text = extract_full_text(article['url'])
        if full_text:
            print(f"[INFO] Full text extracted ({len(full_text)} chars)")
        else:
            full_text = article.get('description') or ''
            print("[INFO] Using API description as fallback text")

        # Step 2 — generate blog post + LinkedIn draft with Gemini
        generated = generate_with_gemini(title, full_text, article['url'])

        # Step 3 — save both files
        blog_path, blog_slug = write_blog_post(article, generated['blog_post'])
        li_path = write_linkedin_draft(article, generated['linkedin'], blog_slug)

        print(f"[OK] Blog post saved:      {blog_path}")
        print(f"[OK] LinkedIn draft saved: {li_path}")
        break  # One post per daily run


if __name__ == '__main__':
    update_blog()
