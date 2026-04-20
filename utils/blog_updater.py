"""
blog_updater.py
---------------
Daily automation: fetch a tech news article, extract its full text with
requests, then use Gemini to write a short English summary + dev analysis.
Saves the result as a Markdown file ready for the Flask blog.
Also writes a LinkedIn-ready .txt draft alongside the blog post.
"""

import os
import sys
import requests
from google import genai
from slugify import slugify
from datetime import datetime
import logging

# Configuration
NEWS_API_KEY   = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR     = os.path.join(PROJECT_ROOT, 'data', 'blog_posts')
LINKEDIN_DIR = os.path.join(PROJECT_ROOT, 'data', 'linkedin_drafts')
LOG_DIR      = os.path.join(PROJECT_ROOT, 'data', 'logs')

os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'news_fetch.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_env():
    missing = [k for k in ('NEWS_API_KEY', 'GEMINI_API_KEY') if not os.getenv(k)]
    if missing:
        error_msg = f"[ERROR] Missing environment variables: {', '.join(missing)}"
        print(error_msg)
        logging.error(error_msg)
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
        logging.error(f"NewsAPI request failed: {e}")
        return []


# ---------------------------------------------------------------------------
# Full-text extraction
# ---------------------------------------------------------------------------

def extract_full_text(url: str) -> str:
    """
    Fetch full article content using requests.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()
        return r.text
    except Exception as e:
        logging.warning(f"Could not fetch full content from {url}: {e}")
        return ''


# ---------------------------------------------------------------------------
# Gemini generation
# ---------------------------------------------------------------------------

def generate_with_gemini(title: str, body_text: str, source_url: str) -> dict:
    """
    Ask Gemini to produce a summary and LinkedIn draft.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Prompt for blog summary
    blog_prompt = f"""
You are a technical writer. Read the following article and write a summary in English focused on: how this impacts a Developer or Data Scientist's daily work, practical benefits, and key takeaways. Write in first person as if I wrote this article. Be concise, clear, and engaging. 3 to 5 paragraphs.

ARTICLE TITLE: {title}
ARTICLE CONTENT:
{body_text[:10000]}
"""

    try:
        # Generate Blog Summary
        blog_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=blog_prompt,
        )
        summary = blog_response.text.strip()
        
        if not summary:
            raise ValueError("Gemini returned empty summary")

        # Generate LinkedIn Draft
        li_prompt = f"""
Based on the following summary, create a LinkedIn post:
- Hook sentence (1 line, engaging, in English)
- 3 bullet points with the key takeaways
- Use the following CTA: "I wrote about this on my blog, read the full summary here: https://www.wolflergf.com/blog/{slugify(title)}"
- Optional source line: "Fonte original: {source_url}"

SUMMARY:
{summary}
"""
        li_response = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=li_prompt,
        )
        linkedin_draft = li_response.text.strip()

        return {
            'summary': summary,
            'linkedin': linkedin_draft
        }

    except Exception as e:
        logging.error(f"Gemini generation failed for {title}: {e}")
        return {}


# ---------------------------------------------------------------------------
# File writers
# ---------------------------------------------------------------------------

def write_blog_post(article: dict, summary: str) -> str:
    """Write the .md file."""
    os.makedirs(BLOG_DIR, exist_ok=True)
    slug = slugify(article['title'])
    filepath = os.path.join(BLOG_DIR, f'{slug}.md')
    today = datetime.now().strftime('%Y-%m-%d')
    
    content = f"""---
title: {article['title']}
date: {today}
source_url: {article['url']}
---

{summary}
"""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


def write_linkedin_draft(article: dict, linkedin_text: str) -> str:
    """Write the .txt file."""
    os.makedirs(LINKEDIN_DIR, exist_ok=True)
    slug = slugify(article['title'])
    filepath = os.path.join(LINKEDIN_DIR, f'{slug}.txt')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(linkedin_text)
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def update_blog():
    validate_env()

    articles = get_tech_news()
    if not articles:
        logging.info("No articles returned from NewsAPI.")
        return

    for article in articles:
        title = article.get('title', '')
        url = article.get('url', '')
        
        if not title or not url or '[Removed]' in title:
            continue

        slug = slugify(title)
        blog_path = os.path.join(BLOG_DIR, f'{slug}.md')

        if os.path.exists(blog_path):
            logging.info(f"Skipping already existing article: {slug}")
            continue

        print(f"Processing: {title}")
        
        # 2a. Fetch full content
        full_html = extract_full_text(url)
        if not full_html:
            logging.error(f"Skipping {title}: Could not fetch URL {url}")
            continue

        # 2b. Generate with Gemini
        generated = generate_with_gemini(title, full_html, url)
        if not generated:
            logging.error(f"Skipping {title}: Gemini returned invalid response")
            continue

        # 3 & 4. Save files
        write_blog_post(article, generated['summary'])
        write_linkedin_draft(article, generated['linkedin'])

        logging.info(f"Successfully processed: {title}")
        print(f"Done: {title}")
        # Process one article per run (as per existing logic pattern)
        break


if __name__ == '__main__':
    update_blog()
