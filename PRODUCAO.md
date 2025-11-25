# T2 Web - Guia de Produção

> Instruções completas para colocar o sistema em produção

## 📋 Índice

1. [Requisitos](#requisitos)
2. [Opção 1: Servidor VPS (Recomendado)](#opção-1-servidor-vps)
3. [Opção 2: PythonAnywhere](#opção-2-pythonanywhere)
4. [Opção 3: Heroku](#opção-3-heroku)
5. [Opção 4: Docker](#opção-4-docker)
6. [Configurações de Segurança](#configurações-de-segurança)
7. [Backup e Manutenção](#backup-e-manutenção)

---

## Requisitos

### Mínimos
- **CPU**: 1 core
- **RAM**: 1 GB
- **Disco**: 10 GB
- **SO**: Ubuntu 20.04+ ou similar

### Recomendados
- **CPU**: 2 cores
- **RAM**: 2 GB
- **Disco**: 20 GB
- **SO**: Ubuntu 22.04 LTS

---

## Opção 1: Servidor VPS (Recomendado)

### Passo 1: Preparar Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependências
sudo apt install -y python3.11 python3.11-venv python3-pip nginx postgresql postgresql-contrib git

# Criar usuário para aplicação
sudo adduser t2web
sudo usermod -aG sudo t2web
su - t2web
```

### Passo 2: Configurar PostgreSQL

```bash
# Entrar no PostgreSQL
sudo -u postgres psql

# Criar banco e usuário
CREATE DATABASE t2web_db;
CREATE USER t2web_user WITH PASSWORD 'SUA_SENHA_FORTE_AQUI';
ALTER ROLE t2web_user SET client_encoding TO 'utf8';
ALTER ROLE t2web_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE t2web_user SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE t2web_db TO t2web_user;
\q
```

### Passo 3: Instalar Aplicação

```bash
# Criar diretório
cd /home/t2web
mkdir app
cd app

# Clonar ou fazer upload do projeto
# Se usar git:
git clone SEU_REPOSITORIO .

# Ou fazer upload via SCP/SFTP do arquivo ZIP e extrair:
unzip kanban_contratos.zip
mv kanban_contratos/* .

# Criar ambiente virtual
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### Passo 4: Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env
nano .env
```

Adicionar:

```env
# Django
SECRET_KEY=sua-chave-secreta-muito-longa-e-aleatoria-aqui
DEBUG=False
ALLOWED_HOSTS=seudominio.com,www.seudominio.com,IP_DO_SERVIDOR

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=t2web_db
DB_USER=t2web_user
DB_PASSWORD=SUA_SENHA_FORTE_AQUI
DB_HOST=localhost
DB_PORT=5432

# Email (opcional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu@email.com
EMAIL_HOST_PASSWORD=sua-senha-de-app
```

### Passo 5: Atualizar settings.py para Produção

```bash
nano contratos_project/settings.py
```

Adicionar no início:

```python
import os
from pathlib import Path

# Carregar variáveis de ambiente
SECRET_KEY = os.getenv('SECRET_KEY', 'fallback-key')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DB_ENGINE', 'django.db.backends.sqlite3'),
        'NAME': os.getenv('DB_NAME', BASE_DIR / 'db.sqlite3'),
        'USER': os.getenv('DB_USER', ''),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', ''),
    }
}

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'  # Permite iframes da mesma origem para visualização de anexos
```

### Passo 6: Migrar Banco e Coletar Estáticos

```bash
# Carregar variáveis de ambiente
export $(cat .env | xargs)

# Migrar banco
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Criar superusuário
python manage.py createsuperuser

# Configurar permissões
python configurar_permissoes.py
```

### Passo 7: Configurar Gunicorn

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/t2web.service
```

Adicionar:

```ini
[Unit]
Description=T2 Web Gunicorn daemon
After=network.target

[Service]
User=t2web
Group=www-data
WorkingDirectory=/home/t2web/app
EnvironmentFile=/home/t2web/app/.env
ExecStart=/home/t2web/app/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/t2web/app/t2web.sock \
          contratos_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# Iniciar e habilitar serviço
sudo systemctl start t2web
sudo systemctl enable t2web
sudo systemctl status t2web
```

### Passo 8: Configurar Nginx

```bash
# Criar configuração
sudo nano /etc/nginx/sites-available/t2web
```

Adicionar:

```nginx
server {
    listen 80;
    server_name seudominio.com www.seudominio.com;

    client_max_body_size 20M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /home/t2web/app/staticfiles/;
    }

    location /media/ {
        alias /home/t2web/app/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/t2web/app/t2web.sock;
    }
}
```

```bash
# Ativar site
sudo ln -s /etc/nginx/sites-available/t2web /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Passo 9: Configurar SSL (HTTPS)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx -y

# Obter certificado
sudo certbot --nginx -d seudominio.com -d www.seudominio.com

# Testar renovação automática
sudo certbot renew --dry-run
```

### Passo 10: Configurar Firewall

```bash
# Configurar UFW
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable
sudo ufw status
```

---

## Opção 2: PythonAnywhere

### Passo 1: Criar Conta
1. Acesse https://www.pythonanywhere.com
2. Crie conta (plano pago necessário para domínio próprio)

### Passo 2: Upload do Projeto
```bash
# No console do PythonAnywhere
cd ~
unzip kanban_contratos.zip
mv kanban_contratos t2web
cd t2web
```

### Passo 3: Criar Ambiente Virtual
```bash
mkvirtualenv --python=/usr/bin/python3.11 t2web-env
pip install -r requirements.txt
```

### Passo 4: Configurar Web App
1. Web → Add a new web app
2. Manual configuration → Python 3.11
3. Configurar WSGI file
4. Configurar static files
5. Configurar media files

### Passo 5: Configurar Banco
- Usar MySQL fornecido pelo PythonAnywhere
- Atualizar settings.py com credenciais

---

## Opção 3: Heroku

### Passo 1: Preparar Projeto

Criar `Procfile`:
```
web: gunicorn contratos_project.wsgi --log-file -
```

Criar `runtime.txt`:
```
python-3.11.0
```

Atualizar `requirements.txt`:
```bash
pip freeze > requirements.txt
```

### Passo 2: Deploy

```bash
# Instalar Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# Login
heroku login

# Criar app
heroku create t2web-contratos

# Adicionar PostgreSQL
heroku addons:create heroku-postgresql:mini

# Configurar variáveis
heroku config:set SECRET_KEY=sua-chave-secreta
heroku config:set DEBUG=False

# Deploy
git push heroku main

# Migrar banco
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python configurar_permissoes.py
```

---

## Opção 4: Docker

### Dockerfile

```dockerfile
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "contratos_project.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: t2web_db
      POSTGRES_USER: t2web_user
      POSTGRES_PASSWORD: senha_forte
    
  web:
    build: .
    command: gunicorn contratos_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:latest
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Deploy com Docker

```bash
# Build e iniciar
docker-compose up -d --build

# Migrar banco
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Configurar permissões
docker-compose exec web python configurar_permissoes.py
```

---

## Configurações de Segurança

### 1. Gerar SECRET_KEY Segura

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 2. Configurar HTTPS

- Sempre use SSL/TLS em produção
- Redirecione HTTP para HTTPS
- Configure HSTS

### 3. Configurar CORS (se necessário)

```bash
pip install django-cors-headers
```

Adicionar em settings.py:
```python
INSTALLED_APPS = [
    ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    ...
]

CORS_ALLOWED_ORIGINS = [
    "https://seudominio.com",
]
```

### 4. Limitar Taxa de Requisições

```bash
pip install django-ratelimit
```

### 5. Configurar Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/t2web/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

---

## Backup e Manutenção

### Backup Automático do Banco

```bash
# Criar script de backup
nano /home/t2web/backup.sh
```

```bash
#!/bin/bash
BACKUP_DIR="/home/t2web/backups"
DATE=$(date +%Y%m%d_%H%M%S)
FILENAME="t2web_backup_$DATE.sql"

mkdir -p $BACKUP_DIR

pg_dump -U t2web_user t2web_db > $BACKUP_DIR/$FILENAME

# Manter apenas últimos 7 dias
find $BACKUP_DIR -name "*.sql" -mtime +7 -delete

echo "Backup concluído: $FILENAME"
```

```bash
# Tornar executável
chmod +x /home/t2web/backup.sh

# Agendar no cron (diariamente às 2h)
crontab -e
```

Adicionar:
```
0 2 * * * /home/t2web/backup.sh
```

### Backup dos Arquivos (Media)

```bash
# Adicionar ao script de backup
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /home/t2web/app/media/
```

### Monitoramento

```bash
# Instalar htop
sudo apt install htop

# Monitorar logs
sudo journalctl -u t2web -f

# Monitorar Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Atualização do Sistema

```bash
# Fazer backup antes
/home/t2web/backup.sh

# Atualizar código
cd /home/t2web/app
git pull  # ou fazer upload da nova versão

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar dependências
pip install -r requirements.txt

# Migrar banco
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic --noinput

# Reiniciar serviço
sudo systemctl restart t2web
```

---

## Checklist de Produção

- [ ] DEBUG=False
- [ ] SECRET_KEY forte e única
- [ ] ALLOWED_HOSTS configurado
- [ ] Banco PostgreSQL/MySQL
- [ ] Gunicorn configurado
- [ ] Nginx configurado
- [ ] SSL/HTTPS ativo
- [ ] Firewall configurado
- [ ] Backup automático
- [ ] Logs configurados
- [ ] Monitoramento ativo
- [ ] Domínio apontado
- [ ] Email configurado
- [ ] Permissões de arquivo corretas
- [ ] Superusuário criado
- [ ] Grupos de permissões criados

---

## Suporte

Para problemas ou dúvidas:
- Documentação Django: https://docs.djangoproject.com
- Nginx: https://nginx.org/en/docs/
- PostgreSQL: https://www.postgresql.org/docs/

---

**Versão**: 2.0  
**Atualizado**: Outubro 2025



## ⚠️ Observações Importantes

### Formato do Campo `valor_aluguel`

O campo `valor_aluguel` é um `DecimalField` e espera que os valores sejam enviados com **ponto** como separador decimal (ex: `1500.50`).

Para garantir que o formulário de edição funcione corretamente em diferentes localidades, o template `editar.html` usa `{% localize off %}` para forçar a exibição do valor com ponto. Certifique-se de que essa configuração seja mantida.

