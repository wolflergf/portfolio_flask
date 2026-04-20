# 🦞 picoclaw-portfolio-flask

Modern, dynamic portfolio website built with **Flask 3.0**, designed for Computer Science students and Data Scientists. Featuring an AI-powered blog automation system, project showcase, and seamless deployment integration.

---

## ✨ Features

- **🤖 AI-Powered Blog Automation** - Integrated with Gemini Pro to fetch, summarize, and draft content daily.
- **💼 LinkedIn Integration** - Automatically generates and displays LinkedIn sharing drafts for each blog post.
- **📊 Data-Driven Showcase** - Projects, skills, and education managed via simple JSON files.
- **📝 Markdown Blog** - Write posts in Markdown; the system handles rendering, excerpts, and syntax highlighting.
- **✉️ Contact System** - Fully functional contact form with Flask-Mail integration and CSRF protection.
- **📱 Responsive & Modern UI** - Built with the Inter font family and a mobile-first, clean design.
- **🔍 SEO Optimized** - Dynamic meta tags, Open Graph support, and Twitter Cards for every page.

---

## 🚀 Quick Start (Local)

```bash
# Clone repository
git clone https://github.com/wolflergf/portfolio-flask.git
cd portfolio-flask

# Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env  # Then edit .env with your keys

# Run development server
python app.py
```

---

## 🤖 Blog Automation Script

The portfolio includes a sophisticated `utils/blog_updater.py` script designed for cron-job execution (e.g., on Railway or GitHub Actions).

**Capabilities:**
1. **Fetch**: Pulls the latest tech news via NewsAPI.
2. **Scrape**: Extracts full content from source URLs.
3. **Summarize**: Uses Gemini AI to write technical, first-person summaries.
4. **Draft**: Generates a LinkedIn-ready post with hooks and CTAs.
5. **Publish**: Saves directly to the `data/blog_posts/` and `data/linkedin_drafts/` directories.

---

## 📦 Project Structure

```text
portfolio_flask/
├── app.py                  # Flask Application Factory & Routes
├── config.py               # Environment-based Configurations
├── data/
│   ├── blog_posts/         # Markdown articles
│   ├── linkedin_drafts/    # Generated social drafts
│   ├── projects.json       # Project data
│   └── skills.json         # Skills data
├── static/                 # CSS, JS, and Images
├── templates/              # Jinja2 HTML Templates
└── utils/
    ├── blog_updater.py     # AI Automation Engine
    ├── email_sender.py     # Mail utilities
    └── markdown_parser.py  # Blog parsing logic
```

---

## 🔧 Environment Variables

Required variables for full functionality:

```env
# Flask
SECRET_KEY=your_secret_key
FLASK_ENV=production

# Email (Flask-Mail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
CONTACT_EMAIL=your-receiving-email@domain.com

# AI & News (For Blog Automation)
NEWS_API_KEY=your_newsapi_key
GEMINI_API_KEY=your_google_gemini_key
```

---

## 🛠️ Technologies

- **Backend**: Flask 3.0, Gunicorn
- **Frontend**: Jinja2, Vanilla JS, CSS3 (Inter Font)
- **AI/API**: Google Gemini Pro, NewsAPI
- **Tools**: Markdown, Flask-WTF (CSRF), Flask-Mail

---

## 👤 Author

**Wolfler Guzzo Ferreira**
- **Website**: [wolflergf.com](https://wolflergf.com)
- **GitHub**: [@wolflergf](https://github.com/wolflergf)
- **LinkedIn**: [wolflergf](https://linkedin.com/in/wolflergf)

---
*Built and maintained with 🦞 PicoClaw*
