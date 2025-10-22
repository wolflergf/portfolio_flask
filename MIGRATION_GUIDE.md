# Guia de Migração - Do HTML Estático para Flask

Este documento explica como migrar seu portfólio atual (www.wolflergf.com) para a nova versão Flask.

## 📊 Comparação: Antes vs Depois

### Antes (HTML Estático)

**Estrutura:**
```
portfolio/
├── index.html
├── about.html
├── projects.html
├── blog.html
├── contact.html
├── style.css
└── script.js
```

**Problemas:**
- ❌ Código duplicado (header/footer em cada página)
- ❌ Difícil manutenção
- ❌ Sem gerenciamento de dados
- ❌ Formulário de contato não funcional
- ❌ Blog estático sem sistema de posts
- ❌ Projetos hardcoded no HTML

### Depois (Flask Dinâmico)

**Estrutura:**
```
portfolio_flask/
├── app.py                    # Aplicação principal
├── config.py                 # Configurações
├── templates/                # Templates Jinja2
│   ├── base.html            # Template base (DRY)
│   ├── index.html
│   ├── about.html
│   └── ...
├── static/                   # Arquivos estáticos
│   ├── css/
│   ├── js/
│   └── images/
├── data/                     # Dados em JSON
│   ├── projects.json
│   ├── skills.json
│   └── blog_posts/
└── utils/                    # Utilitários
```

**Vantagens:**
- ✅ Template base único (sem duplicação)
- ✅ Fácil manutenção
- ✅ Dados gerenciados em JSON
- ✅ Formulário de contato funcional com email
- ✅ Sistema de blog com Markdown
- ✅ Projetos dinâmicos e escaláveis
- ✅ Páginas de detalhes automáticas
- ✅ SEO otimizado
- ✅ Fácil adicionar novos projetos/posts

---

## 🔄 Processo de Migração

### Passo 1: Backup do Site Atual

```bash
# Fazer backup completo do site atual
# Baixar todos os arquivos do servidor
```

### Passo 2: Personalizar Dados

#### 2.1 Atualizar Projetos

Edite `data/projects.json` com seus projetos reais:

```json
{
  "id": "brain-tumour-classifier",
  "title": "Brain Tumour Classifier",
  "slug": "brain-tumour-classifier",
  "description": "Brain tumour classification system using machine learning",
  "long_description": "Advanced system for classifying brain tumours...",
  "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  "emoji": "🧠",
  "tags": ["Python", "Machine Learning", "OpenCV", "TensorFlow"],
  "github_url": "https://github.com/seu-usuario/brain-tumour",
  "demo_url": "https://brain-tumour.streamlit.app",
  "featured": true,
  "date": "2025-01-15",
  "technologies": ["Python", "TensorFlow", "OpenCV", "Streamlit", "NumPy"]
}
```

**Como adicionar o Brain Tumour App do Streamlit:**
- Mantenha o app no Streamlit (gratuito)
- Adicione o link no `demo_url`
- O portfólio Flask vai linkar para ele

#### 2.2 Atualizar Skills

Edite `data/skills.json`:

```json
{
  "category": "Python",
  "emoji": "🐍",
  "description": "Main language with experience in application development",
  "tags": ["Python", "PyDub", "Automation"]
}
```

#### 2.3 Atualizar Educação

Edite `data/education.json`:

```json
{
  "title": "Computer Science",
  "emoji": "🎓",
  "status": "Undergraduate studies in progress",
  "description": "Studying the fundamentals of computing...",
  "tags": ["Algorithms", "Data Structures", "Software Engineering"]
}
```

#### 2.4 Adicionar Posts de Blog

Crie arquivos Markdown em `data/blog_posts/`:

```markdown
---
title: Meu Primeiro Post
date: 2025-01-20
tags: python, flask, tutorial
---

# Conteúdo do Post

Escreva seu conteúdo aqui em Markdown...
```

### Passo 3: Personalizar Imagens e Assets

```bash
# Copiar imagens do site antigo
cp -r /caminho/antigo/images/* portfolio_flask/static/images/

# Adicionar seu CV
cp seu-cv.pdf portfolio_flask/static/downloads/Wolfler_Guzzo_Ferreira_CV.pdf

# Adicionar foto de perfil
cp foto-perfil.jpg portfolio_flask/static/images/profile.jpg
```

### Passo 4: Configurar Email

1. **Usar Gmail:**
   - Ativar autenticação de 2 fatores
   - Gerar senha de aplicativo
   - Adicionar ao `.env`:
   
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=seu-email@gmail.com
   MAIL_PASSWORD=senha-app-gerada
   CONTACT_EMAIL=wolfler@wolflergf.com
   ```

2. **Testar localmente:**
   ```bash
   python app.py
   # Acessar http://localhost:5000/contact
   # Enviar mensagem de teste
   ```

### Passo 5: Testar Localmente

```bash
cd portfolio_flask
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acessar: `http://localhost:5000`

**Checklist de testes:**
- [ ] Página inicial carrega
- [ ] Navegação entre páginas funciona
- [ ] Projetos aparecem corretamente
- [ ] Página de detalhes de projeto funciona
- [ ] Blog lista posts
- [ ] Post individual abre
- [ ] Formulário de contato envia email
- [ ] Links de redes sociais funcionam
- [ ] Download de CV funciona
- [ ] Responsivo em mobile

### Passo 6: Deploy

Escolha uma plataforma (veja `DEPLOY.md`):

**Opção A: PythonAnywhere (Mais fácil)**
- Gratuito
- Bom para começar
- Domínio: `seu-usuario.pythonanywhere.com`

**Opção B: Railway (Recomendado)**
- $5 crédito grátis/mês
- Deploy automático via Git
- Fácil conectar domínio customizado

**Opção C: VPS (Avançado)**
- Controle total
- Melhor performance
- Requer conhecimento de servidor

### Passo 7: Configurar Domínio

#### Se usar servidor gratuito atual:

1. **Fazer upload via FTP/SFTP:**
   - Conectar ao servidor
   - Upload de todos os arquivos
   - Configurar Python/Flask no servidor

2. **Configurar WSGI:**
   - Criar arquivo `.htaccess` (se Apache)
   - Ou configurar Nginx/Apache para Flask

#### Se migrar para novo servidor:

1. **Atualizar DNS:**
   - Acessar painel do domínio
   - Atualizar registros A/CNAME
   - Apontar para novo servidor

2. **Aguardar propagação:**
   - DNS pode levar até 48h
   - Testar com `nslookup wolflergf.com`

### Passo 8: Configurar SSL

```bash
# Se VPS com Nginx
sudo certbot --nginx -d wolflergf.com -d www.wolflergf.com

# Railway/Render/PythonAnywhere
# SSL é automático, nada a fazer
```

---

## 🔗 Integrando o Brain Tumour App

Você pode manter o app no Streamlit e integrar de 3 formas:

### Opção 1: Link Direto (Recomendado)

No `data/projects.json`:
```json
{
  "id": "brain-tumour-classifier",
  "demo_url": "https://seu-app.streamlit.app",
  ...
}
```

### Opção 2: Iframe

Criar template especial `templates/brain_tumour_embed.html`:
```html
<iframe 
  src="https://seu-app.streamlit.app" 
  width="100%" 
  height="800px"
  frameborder="0">
</iframe>
```

### Opção 3: Migrar para Flask

Se quiser tudo em um lugar:
- Converter interface Streamlit para Flask templates
- Usar Flask-SocketIO para interatividade
- Mais trabalho, mas tudo centralizado

**Recomendação:** Manter no Streamlit (Opção 1) é mais simples e funciona perfeitamente.

---

## 📝 Atualizando Conteúdo

### Adicionar Novo Projeto

1. Edite `data/projects.json`
2. Adicione novo objeto JSON
3. Commit e push (se usar Git)
4. Reload/redeploy

### Adicionar Novo Post

1. Crie arquivo `.md` em `data/blog_posts/`
2. Adicione frontmatter
3. Escreva conteúdo em Markdown
4. Commit e push

### Atualizar Skills/Educação

1. Edite `data/skills.json` ou `data/education.json`
2. Salve
3. Reload aplicação

---

## 🎨 Customização Visual

### Mudar Cores

Edite `static/css/style.css`:

```css
:root {
    --primary-color: #2C3E50;      /* Cor principal */
    --secondary-color: #1ABC9C;    /* Cor secundária */
    --accent-color: #F39C12;       /* Cor de destaque */
    --text-color: #2C3E50;         /* Cor do texto */
    --text-light: #7F8C8D;         /* Texto claro */
    --bg-light: #F8F9FA;           /* Fundo claro */
}
```

### Mudar Fontes

Edite `static/css/style.css`:

```css
@import url('https://fonts.googleapis.com/css2?family=SuaFonte:wght@400;600;700&display=swap');

:root {
    --font-heading: 'SuaFonte', sans-serif;
    --font-body: 'SuaFonte', sans-serif;
}
```

### Adicionar Google Analytics

Edite `templates/base.html`, antes do `</head>`:

```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## ⚡ Melhorias Futuras

### Fase 1 (Imediato)
- [x] Migrar para Flask
- [x] Sistema de templates
- [x] Formulário de contato funcional
- [x] Blog com Markdown
- [x] Gerenciamento de dados em JSON

### Fase 2 (Próximos meses)
- [ ] Admin panel para gerenciar conteúdo
- [ ] Sistema de comentários no blog
- [ ] Newsletter/mailing list
- [ ] Dark mode
- [ ] Multi-idioma (PT/EN)

### Fase 3 (Futuro)
- [ ] Backend completo com banco de dados
- [ ] Autenticação de usuários
- [ ] API REST para projetos
- [ ] Dashboard de analytics
- [ ] Integração com CMS

---

## 🆘 Problemas Comuns

### "Não sei programar em Flask"
- Flask é simples! Você já tem tudo pronto
- Só precisa editar os arquivos JSON
- Veja a documentação no README.md

### "Meu servidor não suporta Python"
- Migre para PythonAnywhere (gratuito)
- Ou use Railway/Render
- Veja opções em DEPLOY.md

### "Perdi meu site antigo"
- Sempre faça backup antes
- Mantenha versão antiga até testar nova
- Use Git para versionamento

### "Formulário não envia email"
- Verifique credenciais SMTP
- Use senha de aplicativo (não senha normal)
- Teste com email pessoal primeiro

---

## 📞 Próximos Passos

1. ✅ Revisar todo o código
2. ✅ Personalizar dados (projetos, skills, etc)
3. ✅ Testar localmente
4. ✅ Escolher plataforma de deploy
5. ✅ Fazer deploy
6. ✅ Configurar domínio
7. ✅ Testar em produção
8. ✅ Divulgar novo portfólio!

---

**Boa sorte com a migração! 🚀**

Se tiver dúvidas, consulte:
- `README.md` - Documentação geral
- `DEPLOY.md` - Guia de deploy
- Documentação Flask: https://flask.palletsprojects.com/

