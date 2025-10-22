import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from config import config
from utils import send_contact_email, mail, load_blog_posts, get_blog_post

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    csrf = CSRFProtect(app)
    mail.init_app(app)
    
    # Load data files
    def load_json(filename):
        """Load JSON data file"""
        filepath = os.path.join(app.root_path, 'data', filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            app.logger.error(f"Data file not found: {filename}")
            return {}
        except json.JSONDecodeError:
            app.logger.error(f"Invalid JSON in file: {filename}")
            return {}
    
    # Context processor to make data available in all templates
    @app.context_processor
    def inject_data():
        """Inject common data into all templates"""
        return {
            'site_name': 'Wolfler Guzzo Ferreira',
            'site_tagline': 'Computer Science Student & Data Scientist',
            'current_year': 2025
        }
    
    # Routes
    @app.route('/')
    def index():
        """Home page"""
        projects_data = load_json('projects.json')
        projects = projects_data.get('projects', [])
        featured_projects = [p for p in projects if p.get('featured', False)][:2]
        
        return render_template('index.html', 
                             featured_projects=featured_projects,
                             page_title='Home')
    
    @app.route('/about')
    def about():
        """About page"""
        education_data = load_json('education.json')
        skills_data = load_json('skills.json')
        
        return render_template('about.html',
                             education=education_data.get('education', []),
                             certifications=education_data.get('certifications', []),
                             objectives=education_data.get('objectives', []),
                             skills=skills_data.get('skills', []),
                             page_title='About')
    
    @app.route('/projects')
    def projects():
        """Projects listing page"""
        projects_data = load_json('projects.json')
        all_projects = projects_data.get('projects', [])
        featured_projects = [p for p in all_projects if p.get('featured', False)]
        other_projects = [p for p in all_projects if not p.get('featured', False)]
        
        # Get all unique tags
        all_tags = set()
        for project in all_projects:
            all_tags.update(project.get('tags', []))
        
        return render_template('projects.html',
                             featured_projects=featured_projects,
                             other_projects=other_projects,
                             all_tags=sorted(all_tags),
                             page_title='Projects')
    
    @app.route('/projects/<slug>')
    def project_detail(slug):
        """Project detail page"""
        projects_data = load_json('projects.json')
        all_projects = projects_data.get('projects', [])
        
        # Find project by slug
        project = next((p for p in all_projects if p.get('slug') == slug), None)
        
        if not project:
            flash('Project not found.', 'error')
            return redirect(url_for('projects'))
        
        # Get related projects (same tags)
        related_projects = []
        project_tags = set(project.get('tags', []))
        for p in all_projects:
            if p['slug'] != slug:
                p_tags = set(p.get('tags', []))
                if project_tags & p_tags:  # Intersection
                    related_projects.append(p)
        related_projects = related_projects[:3]  # Limit to 3
        
        return render_template('project_detail.html',
                             project=project,
                             related_projects=related_projects,
                             page_title=project['title'])
    
    @app.route('/blog')
    def blog():
        """Blog listing page"""
        blog_dir = os.path.join(app.root_path, 'data', 'blog_posts')
        posts = load_blog_posts(blog_dir)
        
        # Get all unique tags
        all_tags = set()
        for post in posts:
            all_tags.update(post.tags)
        
        return render_template('blog.html',
                             posts=posts,
                             all_tags=sorted(all_tags),
                             page_title='Blog')
    
    @app.route('/blog/<slug>')
    def blog_post(slug):
        """Individual blog post page"""
        blog_dir = os.path.join(app.root_path, 'data', 'blog_posts')
        post = get_blog_post(blog_dir, slug)
        
        if not post:
            flash('Blog post not found.', 'error')
            return redirect(url_for('blog'))
        
        # Get recent posts for sidebar
        all_posts = load_blog_posts(blog_dir)
        recent_posts = [p for p in all_posts if p.slug != slug][:5]
        
        return render_template('blog_post.html',
                             post=post,
                             recent_posts=recent_posts,
                             page_title=post.title)
    
    @app.route('/contact', methods=['GET', 'POST'])
    def contact():
        """Contact page with form"""
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name', '').strip()
            email = request.form.get('email', '').strip()
            subject = request.form.get('subject', '').strip()
            message = request.form.get('message', '').strip()
            
            # Basic validation
            if not all([name, email, subject, message]):
                flash('Please fill in all fields.', 'error')
                return render_template('contact.html', page_title='Contact')
            
            # Send email
            success = send_contact_email(name, email, subject, message)
            
            if success:
                flash('Message sent successfully! I will get back to you soon.', 'success')
                return redirect(url_for('contact'))
            else:
                flash('Error sending message. Please try again or contact me directly via email.', 'error')
        
        return render_template('contact.html', page_title='Contact')
    
    # API endpoints (optional)
    @app.route('/api/projects')
    def api_projects():
        """API endpoint to get all projects as JSON"""
        projects_data = load_json('projects.json')
        return jsonify(projects_data)
    
    @app.route('/api/skills')
    def api_skills():
        """API endpoint to get all skills as JSON"""
        skills_data = load_json('skills.json')
        return jsonify(skills_data)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """404 error handler"""
        return render_template('404.html', page_title='Page Not Found'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500 error handler"""
        return render_template('500.html', page_title='Server Error'), 500
    
    return app

# Create app instance
# For Vercel, always use production config
if os.getenv('VERCEL'):
    app = create_app('production')
else:
    app = create_app(os.getenv('FLASK_ENV', 'development'))

if __name__ == '__main__':
    # Use PORT from environment (Railway, Heroku) or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

