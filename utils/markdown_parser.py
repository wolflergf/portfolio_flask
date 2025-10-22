import os
import re
from datetime import datetime
import markdown
from pathlib import Path

class BlogPost:
    """Represents a blog post parsed from Markdown"""
    
    def __init__(self, filename, title, date, tags, content, slug):
        self.filename = filename
        self.title = title
        self.date = date
        self.tags = tags
        self.content = content
        self.slug = slug
        self.excerpt = self._generate_excerpt()
    
    def _generate_excerpt(self, length=200):
        """Generate excerpt from content"""
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', self.content)
        # Get first N characters
        if len(text) > length:
            return text[:length].rsplit(' ', 1)[0] + '...'
        return text
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'filename': self.filename,
            'title': self.title,
            'date': self.date,
            'tags': self.tags,
            'content': self.content,
            'slug': self.slug,
            'excerpt': self.excerpt
        }

def parse_frontmatter(content):
    """
    Parse YAML-style frontmatter from Markdown content
    
    Expected format:
    ---
    title: Post Title
    date: 2025-01-20
    tags: python, flask, web development
    ---
    
    Content here...
    """
    frontmatter = {}
    body = content
    
    # Check if content starts with ---
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            # Parse frontmatter
            frontmatter_text = parts[1].strip()
            body = parts[2].strip()
            
            for line in frontmatter_text.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Parse tags as list
                    if key == 'tags':
                        frontmatter[key] = [tag.strip() for tag in value.split(',')]
                    # Parse date
                    elif key == 'date':
                        try:
                            frontmatter[key] = datetime.strptime(value, '%Y-%m-%d')
                        except ValueError:
                            frontmatter[key] = value
                    else:
                        frontmatter[key] = value
    
    return frontmatter, body

def load_blog_posts(blog_dir):
    """
    Load all blog posts from a directory
    
    Args:
        blog_dir (str): Path to directory containing Markdown files
        
    Returns:
        list: List of BlogPost objects sorted by date (newest first)
    """
    posts = []
    blog_path = Path(blog_dir)
    
    if not blog_path.exists():
        return posts
    
    for md_file in blog_path.glob('*.md'):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse frontmatter
            frontmatter, body = parse_frontmatter(content)
            
            # Convert Markdown to HTML
            html_content = markdown.markdown(
                body,
                extensions=['fenced_code', 'codehilite', 'tables', 'toc']
            )
            
            # Create slug from filename
            slug = md_file.stem
            
            # Create BlogPost object
            post = BlogPost(
                filename=md_file.name,
                title=frontmatter.get('title', slug.replace('-', ' ').title()),
                date=frontmatter.get('date', datetime.now()),
                tags=frontmatter.get('tags', []),
                content=html_content,
                slug=slug
            )
            
            posts.append(post)
        
        except Exception as e:
            print(f"Error loading blog post {md_file}: {e}")
            continue
    
    # Sort by date (newest first)
    posts.sort(key=lambda x: x.date, reverse=True)
    
    return posts

def get_blog_post(blog_dir, slug):
    """
    Get a specific blog post by slug
    
    Args:
        blog_dir (str): Path to directory containing Markdown files
        slug (str): Slug of the post to retrieve
        
    Returns:
        BlogPost or None: BlogPost object if found, None otherwise
    """
    posts = load_blog_posts(blog_dir)
    for post in posts:
        if post.slug == slug:
            return post
    return None

