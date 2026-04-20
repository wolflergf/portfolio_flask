# Portfolio Flask - Wolfler Guzzo Ferreira

Modern, dynamic portfolio website built with Flask, featuring blog, projects showcase, and contact form.

---

## ✨ Features

- **Dynamic Content Management** - Projects, skills, and education managed via JSON files
- **Blog System** - Write posts in Markdown with automatic rendering
- **Contact Form** - Functional contact form with email integration
- **Responsive Design** - Mobile-friendly layout
- **Modern Typography** - Inter font for professional appearance
- **SEO Optimized** - Meta tags, Open Graph, and Twitter Cards
- **Project Showcase** - Detailed project pages with tags and links

---

## 🚀 Quick Start (Local)

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/portfolio-flask.git
cd portfolio-flask

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run application
python app.py

# Open http://localhost:5000
```

---

## 🚂 Deploy to Railway (Recommended)

This project is configured for **Railway** deployment.

### **Quick Deploy:**

1. Push to GitHub
2. Create Railway project from GitHub repo
3. Configure environment variables
4. Generate domain
5. Done! 🎉

**Detailed guide:** See `RAILWAY_DEPLOY.md`

---

## 📦 Project Structure

```
portfolio_flask/
├── app.py                  # Main Flask application
├── config.py               # Configuration
├── Procfile                # Railway config
├── requirements.txt        # Dependencies
├── templates/              # HTML templates
├── static/                 # CSS, JS, images
├── data/                   # JSON data files
└── utils/                  # Utility modules
```

---

## 🎨 Customization

### **Projects:** Edit `data/projects.json`
### **Skills:** Edit `data/skills.json`
### **Education:** Edit `data/education.json`
### **Blog:** Create `.md` files in `data/blog_posts/`
### **Assets:** Add to `static/images/` and `static/downloads/`

---

## 🔧 Environment Variables

```env
SECRET_KEY=your-secret-key
FLASK_ENV=production
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
CONTACT_EMAIL=contact@yourdomain.com
```

---

## 🛠️ Technologies

- Flask 3.0
- Flask-WTF
- Flask-Mail
- Markdown
- Gunicorn
- Inter Font

---

## 📚 Documentation

- **Railway Deploy:** `RAILWAY_DEPLOY.md` (Complete guide)
- **Migration:** `MIGRATION_GUIDE.md`
- **General Deploy:** `DEPLOY.md`

---

## 👤 Author

**Wolfler Guzzo Ferreira**
- Website: https://wolflergf.com
- GitHub: [@wolflergf](https://github.com/wolflergf)

---

**Built with ❤️ using Flask**


## Blog Automation Upgrade

The `blog_updater.py` script has been upgraded to:
1. Fetch full article content.
2. Generate professional summaries using Gemini AI.
3. Create LinkedIn drafts automatically.
4. Log errors and skips to `data/logs/news_fetch.log`.
5. Avoid duplicate posts by checking existing slugs.
