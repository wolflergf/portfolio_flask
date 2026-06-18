"""
blog_updater.py
---------------
Refactored for peak architectural performance and stability.
Handles 429 Resource Exhausted errors with exponential backoff.
Uses relative pathing from script location for portability.
"""

import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from google import genai
from slugify import slugify
from datetime import datetime
import logging
try:
    from dotenv import load_dotenv
    # Load environment variables from .env file 
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using system enviroment varibles.")

# Configuration
NEWS_API_KEY   = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Use script location to determine paths
# In GitHub Actions with working-directory: portfolio_flask
# SCRIPT_DIR will be /home/runner/work/repo/repo/portfolio_flask/utils
SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) # portfolio_flask/
BLOG_DIR     = os.path.join(PROJECT_ROOT, 'data', 'blog_posts')
LINKEDIN_DIR = os.path.join(PROJECT_ROOT, 'data', 'linkedin_drafts')
LOG_DIR      = os.path.join(PROJECT_ROOT, 'data', 'logs')

os.makedirs(BLOG_DIR, exist_ok=True)
os.makedirs(LINKEDIN_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

print(f"DEBUG: SCRIPT_DIR is {SCRIPT_DIR}")
print(f"DEBUG: PROJECT_ROOT is {PROJECT_ROOT}")
print(f"DEBUG: BLOG_DIR absolute path is {os.path.abspath(BLOG_DIR)}")
logging.basicConfig(
    filename=os.path.join(LOG_DIR, 'news_fetch.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def validate_env():
    missing = [k for k in ('NEWS_API_KEY', 'GEMINI_API_KEY') if not os.getenv(k)]
    if missing:
        logging.error(f"Missing environment variables: {missing}")

def get_tech_news() -> list[dict]:
    url = (
        'https://newsapi.org/v2/everything'
        '?q=AI+OR+"machine+learning"+OR+Python+OR+"data+science"'
        '&language=en'
        '&sortBy=publishedAt'
        '&pageSize=5'
        f'&apiKey={NEWS_API_KEY}'
    )
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return r.json().get('articles', [])
    except Exception as e:
        logging.error(f"NewsAPI failed: {e}")
        return []

def clean_extract(url: str) -> str:
    """Aggressively strip HTML to save tokens and stay within free tier limits."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, timeout=15, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, 'html.parser')
        
        # Remove non-content elements
        for s in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']): 
            s.decompose()
            
        # Extract text from main content areas if possible
        main = soup.find('main') or soup.find('article') or soup.body
        text = main.get_text(separator=' ', strip=True) if main else soup.get_text(separator=' ', strip=True)
        
        return text[:8000]
    except Exception as e:
        logging.warning(f"Extraction failed for {url}: {e}")
        return ''

def generate_with_backoff(client, model, contents, retries=3, initial_delay=10):
    """Exponential backoff for Gemini API 429 errors."""
    for i in range(retries):
        try:
            response = client.models.generate_content(model=model, contents=contents)
            return response
        except Exception as e:
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                delay = initial_delay * (2 ** i)
                logging.warning(f"Quota exceeded. Retrying in {delay}s... (Attempt {i+1}/{retries})")
                time.sleep(delay)
            else:
                logging.error(f"Gemini API error: {e}")
                raise e
    return None

def generate_content(title, body, url):
    client = genai.Client(api_key=GEMINI_API_KEY)
    system_instruction = (
        "You are a technical writer. Read the following article and write a summary in English focused on: "
        "how this impacts a Developer or Data Scientist's daily work, practical benefits, and key takeaways. "
        "Write in first person as if I wrote this article. Be concise, clear, and engaging. 3 to 5 paragraphs."
    )
    
    prompt = f"{system_instruction}\n\nARTICLE TITLE: {title}\nARTICLE CONTENT:\n{body}"
    
    try:
        response = generate_with_backoff(client, 'gemini-2.5-flash', prompt)
        if not response: return None
        summary = response.text.strip()
        
        li_prompt = f"Create a short, engaging LinkedIn post based on this summary. Include a link to the blog: https://www.wolflergf.com/blog/{slugify(title)}\n\nSUMMARY:\n{summary}"
        li_response = generate_with_backoff(client, 'gemini-2.5-flash', li_prompt)
        
        return {'summary': summary, 'linkedin': li_response.text.strip() if li_response else ""}
    except Exception as e:
        logging.error(f"Generation failed: {e}")
        return None

def update_blog():
    validate_env()
    articles = get_tech_news()
    if not articles:
        print("DEBUG: No articles fetched from NewsAPI.")
        return

    for article in articles:
        title = article.get('title')
        url = article.get('url')
        if not title or not url or '[Removed]' in title: continue
        
        slug = slugify(title)
        blog_filename = f'{slug}.md'
        blog_path = os.path.join(BLOG_DIR, blog_filename)
        
        if os.path.exists(blog_path):
            print(f"DEBUG: Skipping {title}, file already exists.")
            continue
        
        print(f"Refactoring content for: {title}")
        body = clean_extract(url)
        if not body:
            print(f"DEBUG: Extraction failed for {url}")
            continue
        
        generated = generate_content(title, body, url)
        if not generated:
            print(f"DEBUG: AI generation failed for {title}")
            continue
        
        # Ensure directories exist right before writing
        os.makedirs(BLOG_DIR, exist_ok=True)
        os.makedirs(LINKEDIN_DIR, exist_ok=True)
        
        print(f"DEBUG: Writing blog to {os.path.abspath(blog_path)}")
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: {title}\ndate: {datetime.now().strftime('%Y-%m-%d')}\nsource_url: {url}\n---\n\n{generated['summary']}\n\n[Read the full article here]({url})")
            
        linkedin_path = os.path.join(LINKEDIN_DIR, f'{slug}.txt')
        print(f"DEBUG: Writing LinkedIn draft to {os.path.abspath(linkedin_path)}")
        with open(linkedin_path, 'w', encoding='utf-8') as f:
            f.write(generated['linkedin'])
            
        print(f"Successfully updated blog with: {title}")
        # break # Removed break to allow multiple updates per run if applicable

if __name__ == '__main__':
    update_blog()
