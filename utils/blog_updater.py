import os
import requests
import google.generativeai as genai
from slugify import slugify
from datetime import datetime

# Configurações (Serão lidas dos Secrets do GitHub)
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

def get_tech_news():
    url = f'https://newsapi.org/v2/everything?q=AI+Artificial+Intelligence+Python+DataScience&language=en&sortBy=publishedAt&pageSize=5&apiKey={NEWS_API_KEY}'
    response = requests.get(url)
    return response.json().get('articles', [])

def summarize_with_gemini(title, description, url):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Aja como um especialista em tecnologia e Ciência de Dados. 
    Resuma a seguinte notícia de forma profissional e instigante para um blog de portfólio.
    Traduza tudo para o Português do Brasil.
    
    Título Original: {title}
    Descrição: {description}
    
    Formate a resposta em Markdown. No final, adicione uma seção 'Minha análise' explicando por que isso é importante para desenvolvedores Python ou Cientistas de Dados.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return f"{description}\n\n[Leia mais aqui]({url})"

def update_blog():
    articles = get_tech_news()
    
    for art in articles:
        title = art['title']
        if not title or "[Removed]" in title: continue
        
        slug = slugify(title)
        filepath = f"data/blog_posts/{slug}.md"
        
        # Evita duplicados
        if os.path.exists(filepath):
            continue
            
        print(f"Processando: {title}")
        summary = summarize_with_gemini(title, art['description'], art['url'])
        
        content = f"""---
title: "{title}"
date: {datetime.now().strftime('%Y-%m-%d')}
summary: "{art['description'][:150]}..."
image: {art.get('urlToImage', 'https://via.placeholder.com/800x400')}
---

{summary}

---
*Fonte original: [{title}]({art['url']})*
"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # Processa apenas um por execução para manter o blog fresco
        break 

if __name__ == "__main__":
    update_blog()