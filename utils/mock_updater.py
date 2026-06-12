import os
import sys
import time
from google import genai
from slugify import slugify
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration (Ensure these are set in your environment if running for real)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

SCRIPT_DIR   = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
BLOG_DIR     = os.path.join(PROJECT_ROOT, 'data', 'blog_posts')
LINKEDIN_DIR = os.path.join(PROJECT_ROOT, 'data', 'linkedin_drafts')

os.makedirs(BLOG_DIR, exist_ok=True)
os.makedirs(LINKEDIN_DIR, exist_ok=True)

def generate_content(title, body):
    client = genai.Client(api_key=GEMINI_API_KEY)
    system_instruction = (
        "You are a technical writer. Read the following article and write a summary in English focused on: "
        "how this impacts a Developer or Data Scientist's daily work, practical benefits, and key takeaways. "
        "Write in first person as if I wrote this article. Be concise, clear, and engaging. 3 to 5 paragraphs."
    )
    
    prompt = f"{system_instruction}\n\nARTICLE TITLE: {title}\nARTICLE CONTENT:\n{body}"
    
    try:
        response = client.models.generate_content(model='gemini-2.0-flash', contents=prompt)
        summary = response.text.strip()
        
        li_prompt = f"Create a short, engaging LinkedIn post based on this summary. Include a link to the blog: https://www.wolflergf.com/blog/{slugify(title)}\n\nSUMMARY:\n{summary}"
        li_response = client.models.generate_content(model='gemini-2.0-flash', contents=li_prompt)
        
        return {'summary': summary, 'linkedin': li_response.text.strip() if li_response else ""}
    except Exception as e:
        print(f"Generation failed: {e}")
        return None

def run_mock():
    # Mock data from Towards Data Science
    mock_articles = [
        {
            "title": "When GPU Utilization Lies: The Hidden Systems Problem Slowing Modern AI",
            "body": "Modern AI workloads often show high GPU utilization in monitoring tools like nvidia-smi, but this doesn't always translate to actual computational throughput. The issue often lies in memory bottlenecks, data loading stalls, or inefficient kernel launches. For a data scientist, understanding the difference between 'busy' and 'productive' GPU cycles is critical for optimizing training costs and speed. This article explores how average utilization can be a deceptive metric and how to look deeper into system-level bottlenecks."
        }
    ]

    for article in mock_articles:
        title = article['title']
        body = article['body']
        slug = slugify(title)
        blog_path = os.path.join(BLOG_DIR, f'{slug}.md')
        
        print(f"Processing: {title}")
        generated = generate_content(title, body)
        if not generated:
            continue
            
        with open(blog_path, 'w', encoding='utf-8') as f:
            f.write(f"---\ntitle: {title}\ndate: {datetime.now().strftime('%Y-%m-%d')}\nsource_url: https://towardsdatascience.com/latest/\n---\n\n{generated['summary']}")
            
        linkedin_path = os.path.join(LINKEDIN_DIR, f'{slug}.txt')
        with open(linkedin_path, 'w', encoding='utf-8') as f:
            f.write(generated['linkedin'])
            
        print(f"SUCCESS: Created {blog_path}")

if __name__ == '__main__':
    if not GEMINI_API_KEY:
        print("ERROR: GEMINI_API_KEY not set.")
    else:
        run_mock()
