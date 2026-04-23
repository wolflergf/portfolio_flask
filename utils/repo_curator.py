"""
repo_curator.py
---------------
Weekly automation: scrape GitHub Trending for Python + Machine Learning,
pick the top 3 repos, then use Gemini to write a comparison blog post.
Handles 429 errors with exponential backoff.
"""

import os
import sys
import time
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

def validate_env():
    if not GEMINI_API_KEY:
        print("[ERROR] GEMINI_API_KEY not set")
        sys.exit(1)

def generate_with_backoff(client, model, contents, retries=3, initial_delay=15):
    """Exponential backoff for Gemini API 429 errors."""
    for i in range(retries):
        try:
            response = client.models.generate_content(model=model, contents=contents)
            return response
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                delay = initial_delay * (2 ** i)
                print(f"[WARNING] Quota exceeded. Retrying in {delay}s... (Attempt {i+1}/{retries})")
                time.sleep(delay)
            else:
                print(f"[ERROR] Gemini API error: {e}")
                raise e
    return None

def scrape_trending(topic: str, limit: int = 5) -> list[dict]:
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
            name_tag = article.select_one('h2 a')
            if not name_tag: continue
            repo_path = name_tag['href'].strip('/')
            repo_name = repo_path.replace('/', ' / ')
            desc_tag  = article.select_one('p')
            desc      = desc_tag.get_text(strip=True) if desc_tag else 'No description.'
            stars_tag = article.select_one('a[href$="/stargazers"]')
            stars     = stars_tag.get_text(strip=True) if stars_tag else '?'
            week_tag  = article.select_one('span.d-inline-block.float-sm-right')
            stars_week = week_tag.get_text(strip=True) if week_tag else '?'
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
    python_repos = scrape_trending('python', limit=10)
    ml_repos     = scrape_trending('machine-learning', limit=10)
    seen   = {}
    for repo in python_repos + ml_repos:
        path = repo['path']
        if path in seen:
            seen[path]['score'] = seen[path].get('score', 1) + 1
        else:
            repo['score'] = 1
            seen[path] = repo
    ranked = sorted(seen.values(), key=lambda r: r['score'], reverse=True)
    return ranked[:limit]

def generate_curator_post(repos: list[dict]) -> dict:
    client = genai.Client(api_key=GEMINI_API_KEY)
    repo_block = '\n\n'.join([
        f"Repo {i+1}: {r['name']}\nURL: {r['url']}\nDescription: {r['description']}\nLanguage: {r['language']}"
        for i, r in enumerate(repos)
    ])

    prompt = f"""You are a senior Data Scientist and Python developer writing a weekly "GitHub Radar" column. 
{repo_block}
Write a Markdown blog post between ===BLOG_START=== and ===BLOG_END=== and a LinkedIn post between ===LINKEDIN_START=== and ===LINKEDIN_END===."""

    try:
        response = generate_with_backoff(client, 'gemini-2.0-flash', prompt)
        if not response: raise ValueError("Gemini failed after retries")
        raw = response.text
        blog_post = raw.split('===BLOG_START===')[1].split('===BLOG_END===')[0]
        linkedin = raw.split('===LINKEDIN_START===')[1].split('===LINKEDIN_END===')[0]
        return {'blog_post': blog_post.strip(), 'linkedin': linkedin.strip()}
    except Exception as e:
        print(f"[WARNING] Gemini failed: {e}")
        return {'blog_post': "## Weekly Roundup", 'linkedin': "New trends on GitHub!"}

def write_blog_post(repos: list[dict], blog_body: str) -> tuple[str, str]:
    os.makedirs(BLOG_DIR, exist_ok=True)
    week  = datetime.now().strftime('%Y-W%V')
    slug  = f'github-radar-{week}'
    today = datetime.now().strftime('%Y-%m-%d')
    content = f"---\ntitle: \"GitHub Radar — Week {datetime.now().strftime('%V, %Y')}\"\ndate: {today}\ntags: [Python, ML, GitHub]\n---\n\n{blog_body}"
    filepath = os.path.join(BLOG_DIR, f'{slug}.md')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    return filepath, slug

def write_linkedin_draft(linkedin_text: str, blog_slug: str) -> str:
    os.makedirs(LINKEDIN_DIR, exist_ok=True)
    week = datetime.now().strftime('%Y-W%V')
    filepath = os.path.join(LINKEDIN_DIR, f'github-radar-{week}.txt')
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{linkedin_text}\n\nhttps://www.wolflergf.com/blog/{blog_slug}")
    return filepath

def curate_repos():
    validate_env()
    repos = get_top_repos(limit=3)
    if not repos: sys.exit(1)
    generated = generate_curator_post(repos)
    write_blog_post(repos, generated['blog_post'])
    write_linkedin_draft(generated['linkedin'], f'github-radar-{datetime.now().strftime("%Y-W%V")}')

if __name__ == '__main__':
    curate_repos()
