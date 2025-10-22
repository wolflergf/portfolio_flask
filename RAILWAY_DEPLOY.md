# Guia Completo de Deploy no Railway

Este projeto está configurado para deploy no **Railway** - a plataforma ideal para aplicações Flask.

---

## 🚂 Por Que Railway?

✅ **Suporte nativo a Flask** - Sem configurações complexas
✅ **Deploy em 2 minutos** - Rápido e simples
✅ **$5 de crédito grátis/mês** - Suficiente para portfólio
✅ **SSL automático** - HTTPS incluído
✅ **Logs excelentes** - Fácil debugar
✅ **Domínio customizado** - Configure seu próprio domínio

---

## 📋 Arquivos Necessários (JÁ INCLUÍDOS)

✅ **Procfile** - Diz ao Railway como rodar a aplicação
✅ **requirements.txt** - Lista todas as dependências Python
✅ **app.py** - Aplicação Flask configurada para Railway
✅ **.gitignore** - Ignora arquivos desnecessários

**Tudo já está pronto!** Você só precisa fazer o deploy.

---

## 🚀 Passo a Passo Completo

### **1. Criar Repositório no GitHub**

#### **Opção A: Via Interface Web (Mais Fácil)**

1. Acesse https://github.com/new
2. Nome: `portfolio-flask`
3. Descrição: `Modern portfolio website built with Flask`
4. Visibilidade: **Public** (recomendado) ou Private
5. **NÃO** marque "Initialize with README"
6. Clique em **"Create repository"**

#### **Opção B: Via Linha de Comando**

```bash
# Navegar até a pasta do projeto
cd portfolio_flask

# Inicializar Git
git init

# Adicionar todos os arquivos
git add .

# Primeiro commit
git commit -m "Initial commit - Flask portfolio for Railway"

# Criar branch main
git branch -M main

# Adicionar remote (SUBSTITUA SEU-USUARIO pelo seu username do GitHub)
git remote add origin https://github.com/SEU-USUARIO/portfolio-flask.git

# Fazer push
git push -u origin main
```

---

### **2. Criar Conta no Railway**

1. Acesse https://railway.app
2. Clique em **"Login"**
3. Escolha **"Login with GitHub"** (recomendado)
4. Autorize Railway a acessar seus repositórios
5. Pronto! Conta criada.

---

### **3. Criar Novo Projeto no Railway**

1. No dashboard do Railway, clique em **"New Project"**

2. Selecione **"Deploy from GitHub repo"**

3. **Autorize Railway** a acessar seus repositórios (se necessário)

4. **Selecione o repositório** `portfolio-flask`

5. Railway vai:
   - ✅ Detectar que é Python/Flask
   - ✅ Ler o `Procfile`
   - ✅ Instalar dependências do `requirements.txt`
   - ✅ Iniciar o build automaticamente

6. **Aguarde 2-3 minutos** enquanto o build acontece

7. Você verá logs em tempo real:
   ```
   Building...
   Installing dependencies...
   Starting application...
   Deployment successful! ✅
   ```

---

### **4. Configurar Variáveis de Ambiente**

**IMPORTANTE:** Configure antes de testar o formulário de contato!

1. No dashboard do Railway, clique no seu projeto

2. Vá na aba **"Variables"**

3. Clique em **"+ New Variable"**

4. Adicione as seguintes variáveis (uma por vez):

| Nome | Valor | Descrição |
|------|-------|-----------|
| `SECRET_KEY` | `[gerar chave forte]` | Chave secreta do Flask |
| `FLASK_ENV` | `production` | Ambiente de produção |
| `MAIL_SERVER` | `smtp.gmail.com` | Servidor SMTP |
| `MAIL_PORT` | `587` | Porta SMTP |
| `MAIL_USE_TLS` | `true` | Usar TLS |
| `MAIL_USERNAME` | `seu-email@gmail.com` | Seu email |
| `MAIL_PASSWORD` | `[senha app Gmail]` | Senha de app do Gmail |
| `CONTACT_EMAIL` | `wolfler@wolflergf.com` | Email de contato |

#### **Como gerar SECRET_KEY:**

```python
# Execute no terminal Python
import secrets
print(secrets.token_hex(32))

# Copie o resultado e use como SECRET_KEY
```

#### **Como gerar senha de app do Gmail:**

1. Acesse https://myaccount.google.com/security
2. Ative **"Verificação em duas etapas"**
3. Vá em **"Senhas de app"**
4. Selecione **"Mail"** e **"Outro (nome personalizado)"**
5. Digite: `Portfolio Flask`
6. Clique em **"Gerar"**
7. Copie a senha gerada (16 caracteres)
8. Use em `MAIL_PASSWORD`

5. Após adicionar todas as variáveis, Railway faz **redeploy automático**

---

### **5. Obter URL do Site**

1. No dashboard do Railway, vá em **"Settings"**

2. Na seção **"Domains"**, clique em **"Generate Domain"**

3. Railway gera automaticamente uma URL:
   ```
   portfolio-flask-production.up.railway.app
   ```

4. **Clique na URL** para abrir seu site! 🎉

5. Verifique se tudo está funcionando:
   - ✅ CSS carrega
   - ✅ Fonte Inter aplicada
   - ✅ Navegação funciona
   - ✅ Projetos aparecem
   - ✅ Blog funciona
   - ✅ Formulário de contato aparece

---

### **6. Configurar Domínio Customizado (Opcional)**

Se você quiser usar `wolflergf.com`:

#### **No Railway:**

1. Vá em **"Settings"** → **"Domains"**

2. Clique em **"Custom Domain"**

3. Digite: `wolflergf.com`

4. Railway mostrará a configuração DNS necessária:
   ```
   Type: CNAME
   Name: @
   Value: seu-projeto.up.railway.app
   ```

#### **No Seu Provedor de Domínio:**

1. Acesse o painel do seu provedor (onde você registrou o domínio)

2. Vá em **"DNS Settings"** ou **"Gerenciar DNS"**

3. Adicione/edite o registro:
   ```
   Type: CNAME
   Name: @ (ou deixe vazio)
   Value: seu-projeto.up.railway.app
   TTL: 3600 (ou automático)
   ```

4. Para `www.wolflergf.com`, adicione também:
   ```
   Type: CNAME
   Name: www
   Value: seu-projeto.up.railway.app
   TTL: 3600
   ```

5. **Salve as alterações**

6. **Aguarde propagação DNS** (5 minutos a 48 horas, geralmente ~1 hora)

7. **SSL automático!** Railway configura HTTPS automaticamente

#### **Testar Propagação DNS:**

```bash
# No terminal
nslookup wolflergf.com

# Deve mostrar o IP do Railway
```

---

## 🔄 Atualizações Futuras

### **Deploy Automático**

Sempre que você fizer mudanças e fazer push para GitHub, Railway faz deploy automático!

```bash
# 1. Fazer alterações nos arquivos
# Exemplo: editar data/projects.json para adicionar novo projeto

# 2. Adicionar ao Git
git add .

# 3. Commit
git commit -m "Adicionar novo projeto"

# 4. Push
git push origin main

# 5. Railway detecta e faz deploy automático! 🎉
```

Você verá o progresso em tempo real no dashboard do Railway.

---

## 📊 Monitoramento

### **Dashboard do Railway**

No dashboard você pode ver:

- **Deployments:** Histórico de todos os deploys
- **Metrics:** CPU, memória, requests
- **Logs:** Logs em tempo real da aplicação
- **Build Logs:** Logs do processo de build

### **Ver Logs em Tempo Real**

1. Vá em **"Deployments"**
2. Clique no deploy mais recente
3. Veja logs em tempo real
4. Útil para debugar problemas

---

## 🐛 Troubleshooting

### **Erro no Build**

**Problema:** Build falha com erro de dependências

**Solução:**
```bash
# Verificar requirements.txt
cat requirements.txt

# Deve conter:
Flask==3.0.0
Flask-WTF==1.2.1
Flask-Mail==0.9.1
python-dotenv==1.0.0
markdown==3.5.1
email-validator==2.1.0
Pillow==10.1.0
gunicorn==21.2.0
```

### **Site não abre**

**Problema:** URL do Railway retorna erro

**Solução:**
1. Verificar logs no Railway
2. Verificar se build foi bem-sucedido
3. Verificar variáveis de ambiente
4. Verificar se `SECRET_KEY` está configurado

### **CSS não carrega**

**Problema:** Site aparece sem estilo

**Solução:**
1. Verificar se pasta `static/` está no repositório:
   ```bash
   git ls-files | grep static
   ```
2. Se não estiver, adicionar:
   ```bash
   git add static/
   git commit -m "Add static files"
   git push
   ```

### **Formulário não envia email**

**Problema:** Formulário não funciona

**Solução:**
1. Verificar variáveis de ambiente no Railway
2. Confirmar senha de app do Gmail
3. Ver logs para mensagens de erro
4. Testar localmente primeiro

### **Erro 500**

**Problema:** Página retorna erro 500

**Solução:**
1. Ver logs no Railway dashboard
2. Procurar por stack trace
3. Verificar se todos os arquivos estão no repositório
4. Verificar variáveis de ambiente

---

## 💰 Custos e Limites

### **Trial Plan (Grátis)**

- **$5 de crédito por mês**
- **~500 horas de execução**
- **Suficiente para portfólio**
- **SSL incluído**
- **Domínio customizado incluído**

### **Uso Estimado do Portfólio:**

- Portfólio pessoal: **~$2-3/mês**
- 100 visitas/dia: **~$1/mês**
- 1000 visitas/dia: **~$3-4/mês**

**Conclusão:** O plano gratuito é mais que suficiente! 💯

### **Se Acabar o Crédito:**

- Railway pausa o projeto
- Você pode adicionar cartão de crédito
- Ou esperar o próximo mês (crédito renova)

---

## ✅ Checklist Completo

### **Antes do Deploy:**
- [x] Arquivos Railway criados (Procfile, etc)
- [ ] Repositório GitHub criado
- [ ] Código enviado para GitHub

### **Durante o Deploy:**
- [ ] Conta Railway criada
- [ ] Projeto criado no Railway
- [ ] Repositório conectado
- [ ] Build bem-sucedido
- [ ] Variáveis de ambiente configuradas
- [ ] Redeploy após variáveis

### **Após o Deploy:**
- [ ] URL gerada
- [ ] Site acessível
- [ ] CSS carregando
- [ ] Navegação funcionando
- [ ] Projetos aparecendo
- [ ] Blog funcionando
- [ ] Formulário testado
- [ ] Email recebido

### **Opcional:**
- [ ] Domínio customizado configurado
- [ ] DNS atualizado
- [ ] HTTPS funcionando
- [ ] Compartilhar nas redes sociais! 🎉

---

## 📚 Recursos Úteis

- **Railway Docs:** https://docs.railway.app
- **Railway Discord:** https://discord.gg/railway
- **Status do Railway:** https://status.railway.app
- **Flask Docs:** https://flask.palletsprojects.com

---

## 🆘 Precisa de Ajuda?

1. **Ver logs no Railway** - Primeira coisa a fazer
2. **Railway Discord** - Comunidade muito ativa
3. **Documentação Railway** - Muito completa
4. **Stack Overflow** - Tag `railway`

---

## 🎉 Pronto!

Seu portfólio Flask estará no ar em poucos minutos!

**Fluxo completo:**
```
GitHub → Railway → Build → Deploy → URL → Domínio → Site no ar! 🚀
```

**Tempo estimado:** 10-15 minutos

Boa sorte com o deploy! 🎊

