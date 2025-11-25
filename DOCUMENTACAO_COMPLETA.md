# T2 Web - Sistema de Contratos - Documentação Completa

**Versão**: 2.3  
**Data**: 08/10/2025  
**Status**: Produção

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação Rápida](#instalação-rápida)
3. [Configuração](#configuração)
4. [Funcionalidades](#funcionalidades)
5. [Deploy em Produção](#deploy-em-produção)
6. [Solução de Problemas](#solução-de-problemas)
7. [Manutenção](#manutenção)

---

## 🎯 Visão Geral

Sistema Kanban para gerenciamento de contratos de locação com 9 fases, controle de anexos obrigatórios, sistema de permissões e visualização inline de documentos.

### Características Principais

- **Kanban Visual**: 9 colunas com drag & drop
- **Anexos Obrigatórios**: 3 fases com validação
- **Permissões Granulares**: 7 grupos de usuários
- **Visualização Inline**: PDF e imagens sem download
- **Tema Profissional**: Preto e branco com logo T2 Web
- **Login Personalizado**: Com "lembrar usuário"

---

## 🚀 Instalação Rápida

### Requisitos

- Python 3.11+
- Navegador moderno (Chrome, Firefox, Edge)

### Passo a Passo

```bash
# 1. Extrair projeto
unzip kanban_contratos.zip
cd kanban_contratos

# 2. Criar ambiente virtual
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar migrações
python manage.py migrate

# 5. Coletar arquivos estáticos
python manage.py collectstatic --noinput

# 6. Criar superusuário
python manage.py createsuperuser

# 7. Configurar permissões
python configurar_permissoes.py

# 8. Iniciar servidor
python manage.py runserver
```

**Acesse**: http://localhost:8000

---

## ⚙️ Configuração

### Banco de Dados

**Desenvolvimento** (SQLite - padrão):
```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Produção** (PostgreSQL):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 't2web_db',
        'USER': 't2web_user',
        'PASSWORD': 'senha-forte-aqui',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Variáveis de Ambiente

Crie arquivo `.env`:
```env
SECRET_KEY=sua-chave-secreta-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com
DB_NAME=t2web_db
DB_USER=t2web_user
DB_PASSWORD=senha-forte
```

### Arquivos Estáticos

```bash
# Desenvolvimento
python manage.py collectstatic

# Produção (Nginx)
STATIC_ROOT = '/var/www/t2web/static/'
MEDIA_ROOT = '/var/www/t2web/media/'
```

---

## 🎯 Funcionalidades

### 1. Kanban com 9 Fases

| Fase | Descrição |
|------|-----------|
| Validação de dados | Verificação inicial |
| Análise de crédito | 3 anexos obrigatórios |
| Elaboração do contrato | Preparação de documentos |
| Requisição de vistoria | Laudo obrigatório |
| Minuta em aprovação | Revisão jurídica |
| Assinatura eletrônica | Contrato assinado obrigatório |
| Requisição de lançamento | Financeiro |
| Contrato assinado | Finalizado |
| Contrato cancelado | Terminal |

### 2. Anexos Obrigatórios

**Análise de Crédito** (3 documentos):
- Verificação de Processos Judiciais
- Busca Geral de Protestos
- Consulta de Restrições de Crédito (SPC/SERASA)

**Requisição de Vistoria** (1 documento):
- Laudo de Vistoria

**Assinatura Eletrônica** (1 documento):
- Contrato Assinado

**Validação**: Ao tentar sair da fase sem anexos, modal pede confirmação digitando "CONFIRMAR".

### 3. Sistema de Permissões

7 grupos de usuários com permissões específicas:

| Grupo | Permissões |
|-------|------------|
| **Gerente** | Todas as fases |
| **Analista** | Validação, Elaboração, Minuta |
| **Analista de Crédito** | Análise de Crédito |
| **Jurídico** | Minuta, Assinatura |
| **Vistoriador** | Requisição de Vistoria |
| **Financeiro** | Requisição de Lançamento |
| **Admin** | Todas + configurações |

**Configurar**:
```bash
python configurar_permissoes.py
```

### 4. Visualização de Anexos

- **PDF**: Abre inline no navegador
- **Imagens**: Exibe inline
- **Download**: Botão para baixar individual
- **Download ZIP**: Baixa todos os anexos de uma vez

### 5. Filtros e Busca

- Busca por texto (nome, locatário, imóvel)
- Filtro por responsável
- Filtro por tipo de locatário (PF/PJ)

### 6. Dashboard

- Estatísticas gerais
- Contratos por status
- Contratos atrasados
- Gráficos visuais

---

## 🌐 Deploy em Produção

### Opção 1: VPS (Ubuntu + Nginx + Gunicorn)

#### 1.1. Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install python3.11 python3.11-venv python3-pip nginx postgresql -y

# Criar usuário
sudo adduser t2web
sudo usermod -aG sudo t2web
```

#### 1.2. Configurar PostgreSQL

```bash
sudo -u postgres psql

CREATE DATABASE t2web_db;
CREATE USER t2web_user WITH PASSWORD 'senha-forte-aqui';
ALTER ROLE t2web_user SET client_encoding TO 'utf8';
ALTER ROLE t2web_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE t2web_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE t2web_db TO t2web_user;
\q
```

#### 1.3. Instalar Aplicação

```bash
# Mudar para usuário t2web
su - t2web

# Criar diretório
mkdir -p /home/t2web/app
cd /home/t2web/app

# Upload e extrair projeto
unzip kanban_contratos.zip
cd kanban_contratos

# Ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
pip install gunicorn psycopg2-binary

# Configurar .env
nano .env
```

Arquivo `.env`:
```env
SECRET_KEY=gere-uma-chave-secreta-forte
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,IP-DO-SERVIDOR
DB_NAME=t2web_db
DB_USER=t2web_user
DB_PASSWORD=senha-forte-aqui
DB_HOST=localhost
DB_PORT=5432
```

#### 1.4. Configurar Django

```bash
# Atualizar settings.py para usar .env
pip install python-decouple

# Migrar banco
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic --noinput

# Criar superusuário
python manage.py createsuperuser

# Configurar permissões
python configurar_permissoes.py
```

#### 1.5. Configurar Gunicorn

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/t2web.service
```

Conteúdo:
```ini
[Unit]
Description=T2 Web Gunicorn daemon
After=network.target

[Service]
User=t2web
Group=www-data
WorkingDirectory=/home/t2web/app/kanban_contratos
ExecStart=/home/t2web/app/kanban_contratos/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/t2web/app/kanban_contratos/t2web.sock \
          contratos_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar serviço
sudo systemctl start t2web
sudo systemctl enable t2web
sudo systemctl status t2web
```

#### 1.6. Configurar Nginx

```bash
sudo nano /etc/nginx/sites-available/t2web
```

Conteúdo:
```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/t2web/app/kanban_contratos/staticfiles/;
    }

    location /media/ {
        alias /home/t2web/app/kanban_contratos/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/t2web/app/kanban_contratos/t2web.sock;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/t2web /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 1.7. Configurar SSL (HTTPS)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Renovação automática
sudo certbot renew --dry-run
```

### Opção 2: PythonAnywhere

1. Criar conta em https://www.pythonanywhere.com
2. Upload do projeto
3. Criar Web App (Django)
4. Configurar WSGI
5. Configurar arquivos estáticos
6. Reload

### Opção 3: Heroku

```bash
# Instalar Heroku CLI
# Criar Procfile
echo "web: gunicorn contratos_project.wsgi" > Procfile

# Deploy
heroku login
heroku create t2web-contratos
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

### Opção 4: Docker

```yaml
# docker-compose.yml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: t2web_db
      POSTGRES_USER: t2web_user
      POSTGRES_PASSWORD: senha-forte
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn contratos_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DATABASE_URL=postgresql://t2web_user:senha-forte@db:5432/t2web_db

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

```bash
docker-compose up -d
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```

---

## 🐛 Solução de Problemas

### Problema: Campo "Valor do Aluguel" fica em branco ao editar

**Causa**: DecimalField pode retornar None  
**Solução**: Já corrigido com `|default:''`

### Problema: Login não funciona

**Causa**: Template de login não existe  
**Solução**: Já criado em `templates/registration/login.html`

### Problema: Logout dá erro

**Causa**: URL incorreta (admin:logout)  
**Solução**: Já corrigido para usar `{% url 'logout' %}`

### Problema: Visualização de PDF não funciona

**Causa**: Headers incorretos  
**Solução**: Já corrigido com `Content-Disposition: inline`

### Problema: Permissões não funcionam

**Causa**: Grupos não criados  
**Solução**: Execute `python configurar_permissoes.py`

---

## 🔧 Manutenção

### Backup

```bash
# Backup do banco SQLite
cp db.sqlite3 backup_$(date +%Y%m%d).sqlite3

# Backup PostgreSQL
pg_dump -U t2web_user t2web_db > backup_$(date +%Y%m%d).sql

# Backup de arquivos
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### Atualização

```bash
# Parar serviço
sudo systemctl stop t2web

# Atualizar código
cd /home/t2web/app/kanban_contratos
git pull  # ou upload manual

# Ativar ambiente
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Migrar banco
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic --noinput

# Reiniciar serviço
sudo systemctl start t2web
```

### Monitoramento

```bash
# Ver logs
sudo journalctl -u t2web -f

# Status do serviço
sudo systemctl status t2web

# Logs do Nginx
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log
```

### Limpeza

```bash
# Limpar sessões antigas
python manage.py clearsessions

# Limpar arquivos temporários
find media/ -type f -mtime +90 -delete
```

---

## 📞 Suporte

**Documentação**: README.md, COMO_USAR.md, PERMISSOES.md  
**Versão**: 2.3  
**Data**: 08/10/2025

---

© 2025 T2 Web Real Estate. Todos os direitos reservados.
