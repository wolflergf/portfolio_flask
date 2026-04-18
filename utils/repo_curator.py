"""
repo_curator.py
---------------
Weekly automation: scrape GitHub Trending for Python + Machine Learning,
pick the top 3 repos, then use Gemini to write a comparison blog post.
Also writes a LinkedIn draft.

Run via GitHub Actions every Monday at 09:00 UTC.
"""

import os
import sys
import requests
from bs4 import BeautifulSoup
from google import genai
from slugify import slugify
from datetime import datetime

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG_DIR     = os.path.join(PROJECT_ROOT, 'data', 'blog_posts')
LINKEDIN_DIR = os.path.join(PROJECT_ROOT, 'data', 'linkedin_drafts')

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_env():
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set")
        sys.exit(1)


# ---------------------------------------------------------------------------
# GitHub Trending scraper
# ---------------------------------------------------------------------------

def scrape_trending(topic: str, limit: int = 5) -> list[dict]:
    """
    Scrape github.com/trending/{topic}?since=weekly and return repo dicts.
    Each dict has: name, url, description, stars, language, stars_this_week.
    """
    url = f'https://github.com/trending/{topic}?since=weekly'
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to scrape GitHub Trending ({topic}): {e}")
        return []

    soup  = BeautifulSoup(r.text, 'html.parser')
    repos = []

    for article in soup.select('article.Box-row')[:limit]:
        try:
            # Repo name (owner/repo)
            name_tag = article.select_one('h2 a')
            if not name_tag:
                continue
            repo_path = name_tag['href'].strip('/')          # e.g. "owner/repo"
            repo_name = repo_path.replace('/', ' / ')

            # Description
            desc_tag  = article.select_one('p')
            desc      = desc_tag.get_text(strip=True) if desc_tag else 'No description.'

            # Stars total
            stars_tag = article.select_one('a[href$="/stargazers"]')
            stars     = stars_tag.get_text(strip=True) if stars_tag else '?'

            # Stars gained this week
            week_tag  = article.select_one('span.d-inline-block.float-sm-right')
            stars_week = week_tag.get_text(strip=True) if week_tag else '?'

            # Primary language
            lang_tag  = article.select_one('span[itemprop="programmingLanguage"]')
            language  = lang_tag.get_text(strip=True) if lang_tag else 'Unknown'

            repos.append({
                'name':        repo_name,
                'path':        repo_path,
                'url':         f'https://github.com/{repo_path}',
                'description': desc,
                'stars':       stars,
                'stars_week':  stars_week,
                'language':    language,
            })
        except Exception as e:
            print(f"[WARNING] Error parsing repo entry: {e}")
            continue

    return repos


def get_top_repos(limit: int = 3) -> list[dict]:
    """
    Merge Python and ML trending repos, deduplicate, return top `limit`.
    Prioritises repos that appear in both lists (higher interest signal).
    """
    python_repos = scrape_trending('python', limit=10)
    ml_repos     = scrape_trending('machine-learning', limit=10)

    seen   = {}
    # Repos in both lists get a score of 2, otherwise 1
    for repo in python_repos + ml_repos:
        path = repo['path']
        if path in seen:
            seen[path]['score'] = seen[path].get('score', 1) + 1
        else:
            repo['score'] = 1
            seen[path] = repo

    ranked = sorted(seen.values(), key=lambda r: r['score'], reverse=True)
    return ranked[:limit]


# ---------------------------------------------------------------------------
# Gemini generation
# ---------------------------------------------------------------------------

def generate_curator_post(repos: list[dict]) -> dict:
    """
    Ask Gemini to write a weekly round-up comparing the 3 repos.
    Returns {'blog_post': str, 'linkedin': str}.
    """
    client = genai.Client(api_key=GEMINI_API_KEY)

    repo_block = '\n\n'.join([
        f"Repo {i+1}: {r['name']}\n"
        f"URL: {r['url']}\n"
        f"Description: {r['description']}\n"
        f"Language: {r['language']} | Total stars: {r['stars']} | Stars this week: {r['stars_week']}"
        for i, r in enumerate(repos)
    ])

    prompt = f"""
You are a senior Data Scientist and Python developer writing a weekly "GitHub Radar" column for your portfolio blog.

Here are the 3 hottest Python / Machine Learning repositories on GitHub this week:

{repo_block}

Write TWO pieces of content IN ENGLISH.

===BLOG_START===
[Write a Markdown blog post with this structure:
## What's Trending This Week in Python & ML
- Brief intro (1-2 sentences) about why keeping up with trending repos matters
## The Picks
For each repo write a sub-section (### Repo Name) with:
  - What it does (1-2 sentences, plain language)
  - Why it is gaining traction right now
  - One concrete use case for a Python developer or Data Scientist
## My Take
A 2-3 sentence personal analysis: what does this week's selection reveal about
the direction of the Python / ML ecosystem?
Keep total length 400-600 words. Do NOT repeat URLs — they will be in a table below.]
===BLOG_END===

===LINKEDIN_START===
[Write a short LinkedIn post IN ENGLISH (max 6 sentences):
- Eye-catching opener about this week's GitHub trends
- Mention 1-2 standout repos by name with one sentence on why they matter
- Closing question or CTA to drive engagement
- 4-5 hashtags: #Python #MachineLearning #DataScience #OpenSource #GitHub
No URLs — the blog link will be appended automatically.]
===LINKEDIN_END===
"""

    try:
        response  = client.models.generate_content(
            model='gemini-2.0-flash',
            contents=prompt,
        )
        raw       = response.text
        blog_post = _extract_between(raw, '===BLOG_START===', '===BLOG_END===')
        linkedin  = _extract_between(raw, '===LINKEDIN_START===', '===LINKEDIN_END===')

        if not blog_post:
            raise ValueError("Missing BLOG block in Gemini response")

        return {'blog_post': blog_post.strip(), 'linkedin': linkedin.strip()}

    except Exception as e:
        print(f"[WARNING] Gemini failed: {e}")
        fallback = '\n\n'.join([
            f"### [{r['name']}]({r['url']})\n{r['description']}"
            for r in repos
        ])
        return {
            'blog_post': f"## This Week's Top Repos\n\n{fallback}",
            'linkedin':  "Check out this week's hottest Python repos on GitHub!\n#Python #DataScience"
        }


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


def build_repo_table(repos: list[dict]) -> str:
    """Build a Markdown table summarising the 3 repos."""
    rows = ['| Repository | Language | ⭐ Total | 📈 This Week | Description |',
            '|---|---|---|---|---|']
    for r in repos:
        name_md = f"[{r['name']}]({r['url']})"
        rows.append(
            f"| {name_md} | {r['language']} | {r['stars']} "
            f"| {r['stars_week']} | {r['description'][:60]}... |"
        )
    return '\n'.join(rows)


def write_blog_post(repos: list[dict], blog_body: str) -> tuple[str, str]:
    """Write the weekly curator .md file. Returns (filepath, slug)."""
    os.makedirs(BLOG_DIR, exist_ok=True)
    week  = datetime.now().strftime('%Y-W%V')
    slug  = f'github-radar-{week}'
    today = datetime.now().strftime('%Y-%m-%d')

    repo_table = build_repo_table(repos)
    title_str  = escape_yaml(f'GitHub Radar — Week {datetime.now().strftime("%V, %Y")}')

    content = f"""---
title: "{title_str}"
date: {today}
summary: "The 3 hottest Python & Machine Learning repositories on GitHub this week."
image: https://placehold.co/800x400?text=GitHub+Radar
tags: [Python, Machine Learning, Open Source, GitHub, Weekly]
---

{blog_body}

---

## Quick Reference

{repo_table}
"""
    filepath = os.path.join(BLOG_DIR, f'{slug}.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath, slug


def write_linkedin_draft(linkedin_text: str, blog_slug: str) -> str:
    """Write a ready-to-paste LinkedIn .txt file."""
    os.makedirs(LINKEDIN_DIR, exist_ok=True)
    week     = datetime.now().strftime('%Y-W%V')
    filepath = os.path.join(LINKEDIN_DIR, f'github-radar-{week}.txt')
    today    = datetime.now().strftime('%Y-%m-%d')

    # ⚠️  Replace with your actual Railway domain
    blog_url = f"https://www.wolflergf.com/blog/{blog_slug}"

    content = (
        f"# LinkedIn Draft — GitHub Radar {today}\n"
        f"# Copy everything below this line.\n"
        f"# {'─' * 60}\n\n"
        f"{linkedin_text}\n\n"
        f"Full breakdown on my blog 👉 {blog_url}\n"
    )
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def curate_repos():
    validate_env()

    print("[INFO] Fetching GitHub Trending repos...")
    repos = get_top_repos(limit=3)

    if not repos:
        print("[ERROR] No repos found. Exiting.")
        sys.exit(1)

    for r in repos:
        print(f"  • {r['name']} — {r['stars_week']} stars this week")

    print("[INFO] Generating post with Gemini...")
    generated = generate_curator_post(repos)

    blog_path, blog_slug = write_blog_post(repos, generated['blog_post'])
    li_path = write_linkedin_draft(generated['linkedin'], blog_slug)

    print(f"[OK] Blog post saved:      {blog_path}")
    print(f"[OK] LinkedIn draft saved: {li_path}")


if __name__ == '__main__':
    curate_repos()
