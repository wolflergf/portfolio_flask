# Guia de Deploy - Portfolio Flask

Este documento fornece instruções detalhadas para fazer o deploy do seu portfólio Flask em diferentes plataformas.

## 🚀 Opções de Deploy

### 1. PythonAnywhere (Recomendado para Iniciantes)

**Vantagens:**
- Gratuito para projetos pequenos
- Fácil configuração
- Suporte nativo para Flask
- SSL incluído

**Passos:**

1. **Criar conta no PythonAnywhere**
   - Acesse: https://www.pythonanywhere.com
   - Crie uma conta gratuita

2. **Upload dos arquivos**
   ```bash
   # Opção 1: Via Git
   git clone https://github.com/seu-usuario/portfolio_flask.git
   
   # Opção 2: Upload manual via interface web
   # Files > Upload a file
   ```

3. **Configurar ambiente virtual**
   ```bash
   cd portfolio_flask
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configurar WSGI**
   - Vá em Web > Add a new web app
   - Escolha Flask
   - Edite o arquivo WSGI:
   
   ```python
   import sys
   import os
   
   # Adicionar o diretório do projeto ao path
   project_home = '/home/seu_usuario/portfolio_flask'
   if project_home not in sys.path:
       sys.path = [project_home] + sys.path
   
   # Carregar variáveis de ambiente
   from dotenv import load_dotenv
   load_dotenv(os.path.join(project_home, '.env'))
   
   # Importar a aplicação
   from app import app as application
   ```

5. **Configurar variáveis de ambiente**
   - Na aba Web, adicione variáveis de ambiente:
   ```
   FLASK_ENV=production
   SECRET_KEY=sua-chave-secreta-forte
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=seu-email@gmail.com
   MAIL_PASSWORD=sua-senha-app
   CONTACT_EMAIL=wolfler@wolflergf.com
   ```

6. **Reload da aplicação**
   - Clique em "Reload" no dashboard

7. **Acessar o site**
   - Seu site estará disponível em: `seu_usuario.pythonanywhere.com`

---

### 2. Railway (Moderno e Simples)

**Vantagens:**
- Deploy automático via Git
- SSL gratuito
- Fácil configuração de domínio customizado
- $5 de crédito grátis por mês

**Passos:**

1. **Preparar o projeto**
   
   Criar `Procfile`:
   ```
   web: gunicorn app:app
   ```
   
   Adicionar `gunicorn` ao `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```

2. **Criar conta no Railway**
   - Acesse: https://railway.app
   - Faça login com GitHub

3. **Criar novo projeto**
   - New Project > Deploy from GitHub repo
   - Selecione o repositório do portfolio

4. **Configurar variáveis de ambiente**
   - Settings > Variables
   - Adicione todas as variáveis do `.env`

5. **Deploy automático**
   - Railway detecta automaticamente Flask
   - Deploy acontece automaticamente

6. **Configurar domínio**
   - Settings > Domains
   - Adicione seu domínio customizado
   - Configure DNS conforme instruções

---

### 3. Render (Alternativa ao Heroku)

**Vantagens:**
- Plano gratuito disponível
- SSL automático
- Deploy via Git
- Fácil de usar

**Passos:**

1. **Preparar o projeto**
   
   Criar `build.sh`:
   ```bash
   #!/usr/bin/env bash
   pip install -r requirements.txt
   ```
   
   Criar `render.yaml`:
   ```yaml
   services:
     - type: web
       name: portfolio-flask
       env: python
       buildCommand: pip install -r requirements.txt
       startCommand: gunicorn app:app
       envVars:
         - key: FLASK_ENV
           value: production
         - key: SECRET_KEY
           generateValue: true
   ```

2. **Criar conta no Render**
   - Acesse: https://render.com
   - Faça login com GitHub

3. **Criar Web Service**
   - New > Web Service
   - Conecte o repositório GitHub
   - Configure:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`

4. **Adicionar variáveis de ambiente**
   - Environment > Add Environment Variable
   - Adicione todas as variáveis necessárias

5. **Deploy**
   - Clique em "Create Web Service"
   - Deploy automático será iniciado

---

### 4. VPS (DigitalOcean, Linode, AWS)

**Vantagens:**
- Controle total
- Melhor performance
- Escalável

**Passos básicos:**

1. **Criar servidor Ubuntu**
   ```bash
   # Atualizar sistema
   sudo apt update && sudo apt upgrade -y
   
   # Instalar Python e dependências
   sudo apt install python3.11 python3.11-venv python3-pip nginx -y
   ```

2. **Clonar projeto**
   ```bash
   cd /var/www
   git clone https://github.com/seu-usuario/portfolio_flask.git
   cd portfolio_flask
   ```

3. **Configurar ambiente virtual**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Criar serviço systemd**
   
   `/etc/systemd/system/portfolio.service`:
   ```ini
   [Unit]
   Description=Portfolio Flask App
   After=network.target
   
   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/var/www/portfolio_flask
   Environment="PATH=/var/www/portfolio_flask/venv/bin"
   EnvironmentFile=/var/www/portfolio_flask/.env
   ExecStart=/var/www/portfolio_flask/venv/bin/gunicorn --workers 3 --bind 127.0.0.1:5000 app:app
   
   [Install]
   WantedBy=multi-user.target
   ```

5. **Configurar Nginx**
   
   `/etc/nginx/sites-available/portfolio`:
   ```nginx
   server {
       listen 80;
       server_name wolflergf.com www.wolflergf.com;
   
       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   
       location /static {
           alias /var/www/portfolio_flask/static;
       }
   }
   ```

6. **Ativar site**
   ```bash
   sudo ln -s /etc/nginx/sites-available/portfolio /etc/nginx/sites-enabled/
   sudo systemctl start portfolio
   sudo systemctl enable portfolio
   sudo systemctl restart nginx
   ```

7. **Configurar SSL com Let's Encrypt**
   ```bash
   sudo apt install certbot python3-certbot-nginx -y
   sudo certbot --nginx -d wolflergf.com -d www.wolflergf.com
   ```

---

## 🔐 Segurança em Produção

### Gerar SECRET_KEY forte

```python
import secrets
print(secrets.token_hex(32))
```

### Configurar Email (Gmail)

1. Ativar autenticação de 2 fatores
2. Gerar senha de aplicativo:
   - Google Account > Security > 2-Step Verification > App passwords
3. Usar a senha gerada em `MAIL_PASSWORD`

### Variáveis de ambiente obrigatórias

```env
FLASK_ENV=production
SECRET_KEY=chave-forte-gerada
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=seu-email@gmail.com
MAIL_PASSWORD=senha-app-gerada
CONTACT_EMAIL=wolfler@wolflergf.com
```

---

## 📋 Checklist de Deploy

- [ ] Gerar `SECRET_KEY` forte
- [ ] Configurar `FLASK_ENV=production`
- [ ] Configurar credenciais de email
- [ ] Testar formulário de contato
- [ ] Verificar todas as rotas
- [ ] Configurar domínio customizado
- [ ] Ativar SSL/HTTPS
- [ ] Testar responsividade
- [ ] Verificar performance
- [ ] Configurar backups
- [ ] Adicionar Google Analytics (opcional)
- [ ] Testar em diferentes navegadores

---

## 🔄 Atualização do Site

### Via Git (Railway/Render)
```bash
git add .
git commit -m "Atualização do conteúdo"
git push origin main
# Deploy automático será acionado
```

### PythonAnywhere
```bash
cd portfolio_flask
git pull origin main
# Clicar em "Reload" no dashboard
```

### VPS
```bash
cd /var/www/portfolio_flask
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart portfolio
```

---

## 🆘 Troubleshooting

### Erro 500 - Internal Server Error
- Verificar logs da aplicação
- Verificar variáveis de ambiente
- Verificar permissões de arquivos

### Formulário não envia email
- Verificar credenciais SMTP
- Verificar firewall/portas
- Testar com email de teste

### CSS/JS não carrega
- Verificar configuração de arquivos estáticos
- Limpar cache do navegador
- Verificar paths no Nginx

### Site lento
- Aumentar workers do Gunicorn
- Ativar cache
- Otimizar imagens
- Usar CDN

---

## 📞 Suporte

Para dúvidas sobre deploy:
- Documentação Flask: https://flask.palletsprojects.com/
- Railway Docs: https://docs.railway.app/
- PythonAnywhere Help: https://help.pythonanywhere.com/

---

**Boa sorte com o deploy! 🚀**

