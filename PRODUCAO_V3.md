# Guia de Produção - Sistema Kanban T2 v3.0

**Versão:** 3.0.0 com Cadastro Público  
**Data:** 08 de outubro de 2025

---

## 🚀 Visão Geral

Este documento fornece instruções detalhadas para deploy, configuração e manutenção do **Sistema Kanban de Contratos T2** em um ambiente de produção. A versão 3.0 introduz o **cadastro público de contratos**, permitindo que clientes iniciem o processo sem necessidade de login.

## ✅ Checklist de Deploy

- [ ] **Servidor:** Ubuntu 22.04 ou superior
- [ ] **Banco de Dados:** MySQL 8.0+ ou PostgreSQL 14+
- [ ] **Servidor de Aplicação:** Gunicorn ou uWSGI
- [ ] **Proxy Reverso:** Nginx
- [ ] **Dependências:** Python 3.11+, pip
- [ ] **Certificado SSL:** Let's Encrypt (ou similar)
- [ ] **Variáveis de Ambiente:** Configuradas

---

## ⚙️ Configuração do Ambiente

### 1. Instalar Dependências do Sistema

```bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3-pip nginx mysql-server libmysqlclient-dev
```

### 2. Criar Banco de Dados MySQL

```sql
-- Conectar ao MySQL
sudo mysql

-- Criar banco de dados e usuário
CREATE DATABASE kanban_contratos CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'kanban_user'@'localhost' IDENTIFIED BY 'SuaSenhaSeguraAqui';
GRANT ALL PRIVILEGES ON kanban_contratos.* TO 'kanban_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 3. Configurar Projeto

#### a. Clonar/Extrair Projeto

```bash
# Extrair o pacote
unzip SISTEMA_KANBAN_T2_V3_PRONTO.zip
cd kanban_contratos
```

#### b. Criar Ambiente Virtual

```bash
python3.11 -m venv venv
source venv/bin/activate
```

#### c. Instalar Dependências Python

```bash
pip install -r requirements.txt
```

### 4. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```ini
# /home/ubuntu/kanban_contratos/.env

# Segurança (IMPORTANTE: gere uma nova chave)
# python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
SECRET_KEY='SuaChaveSecretaDjangoAqui'

# Ambiente (False em produção)
DEBUG=False

# Domínios permitidos (separados por vírgula)
ALLOWED_HOSTS='seu_dominio.com,www.seu_dominio.com'

# Banco de Dados MySQL
DB_ENGINE='django.db.backends.mysql'
DB_NAME='kanban_contratos'
DB_USER='kanban_user'
DB_PASSWORD='SuaSenhaSeguraAqui'
DB_HOST='localhost'
DB_PORT='3306'

# E-mail (para notificações futuras)
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST='smtp.seu_provedor.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='seu_email@provedor.com'
EMAIL_HOST_PASSWORD='SuaSenhaDeApp'
```

### 5. Aplicar Migrations e Coletar Estáticos

```bash
# Aplicar migrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Coletar arquivos estáticos
python manage.py collectstatic --noinput
```

---

## 🚀 Servidor de Aplicação (Gunicorn)

### 1. Testar Gunicorn

```bash
gunicorn --bind 0.0.0.0:8000 contratos_project.wsgi
```

### 2. Criar Serviço Systemd para Gunicorn

Crie o arquivo `/etc/systemd/system/gunicorn.service`:

```ini
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/kanban_contratos
ExecStart=/home/ubuntu/kanban_contratos/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/home/ubuntu/kanban_contratos/contratos_project.sock \
          contratos_project.wsgi:application

[Install]
WantedBy=multi-user.target
```

### 3. Iniciar e Habilitar Gunicorn

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Verificar status
sudo systemctl status gunicorn
```

---

## 🌐 Proxy Reverso (Nginx)

### 1. Criar Configuração do Nginx

Crie o arquivo `/etc/nginx/sites-available/kanban_contratos`:

```nginx
server {
    listen 80;
    server_name seu_dominio.com www.seu_dominio.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /home/ubuntu/kanban_contratos;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/kanban_contratos/contratos_project.sock;
    }
}
```

### 2. Habilitar Site e Testar Nginx

```bash
# Criar link simbólico
sudo ln -s /etc/nginx/sites-available/kanban_contratos /etc/nginx/sites-enabled

# Testar configuração
sudo nginx -t

# Reiniciar Nginx
sudo systemctl restart nginx
```

### 3. Configurar SSL com Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu_dominio.com -d www.seu_dominio.com
```

---

## 🔄 Atualizações e Manutenção

### 1. Fazer Backup

```bash
# Backup do banco de dados
mysqldump -u kanban_user -p kanban_contratos > backup_db_$(date +%Y%m%d).sql

# Backup dos arquivos
tar -czf backup_app_$(date +%Y%m%d).tar.gz /home/ubuntu/kanban_contratos
```

### 2. Aplicar Atualizações

```bash
# Parar Gunicorn
sudo systemctl stop gunicorn

# Ativar ambiente virtual
source venv/bin/activate

# Puxar/extrair novas versões
# ... (git pull ou unzip)

# Instalar novas dependências
pip install -r requirements.txt

# Aplicar migrations
python manage.py migrate

# Coletar estáticos
python manage.py collectstatic --noinput

# Reiniciar Gunicorn
sudo systemctl start gunicorn
```

### 3. Monitorar Logs

```bash
# Logs do Gunicorn
sudo journalctl -u gunicorn

# Logs do Nginx
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
```

---

## 🔐 Segurança

### 1. `SECRET_KEY`
**NUNCA** use a chave padrão em produção. Gere uma nova e armazene no `.env`.

### 2. `DEBUG = False`
**SEMPRE** `False` em produção para evitar exposição de informações sensíveis.

### 3. `ALLOWED_HOSTS`
Liste **APENAS** os domínios que servirão a aplicação.

### 4. Permissões de Arquivos

```bash
# Restringir acesso ao .env
chmod 600 .env

# Definir permissões para o diretório do projeto
sudo chown -R ubuntu:www-data /home/ubuntu/kanban_contratos
find /home/ubuntu/kanban_contratos -type d -exec chmod 750 {} \;
find /home/ubuntu/kanban_contratos -type f -exec chmod 640 {} \;
```

### 5. Firewall (UFW)

```bash
sudo ufw allow 'Nginx Full'
sudo ufw allow 'OpenSSH'
sudo ufw enable
```

---

## 🎨 Personalização

### Alterar Cores do Tema

Edite as variáveis CSS em `/static/css/t2_theme.css`:

```css
:root {
    --t2-azul: #5B7FDB;
    --t2-verde: #5EADA5;
    --t2-amarelo: #F5B85F;
    --t2-laranja: #F58B5F;
}
```

Após alterar, execute `collectstatic` e reinicie o Gunicorn.

### Alterar Logo

Substitua o arquivo `/static/img/logo.png`.

---

## 🔗 URL do Cadastro Público

Após o deploy, o formulário de cadastro público estará disponível em:

**`https://seu_dominio.com/cadastro/`**

Divulgue este link para seus clientes.

---

## 📊 Funcionalidades da v3.0

- **Cadastro Público:** Formulário acessível sem login.
- **Status Inicial Fixo:** Novos cadastros entram em "Validação de Dados".
- **Campos de Contato:** Email e telefone agora são campos de texto.
- **Notificação de Sucesso:** Página de confirmação com resumo dos dados.
- **Segurança:** Proteção CSRF no formulário público.

---

## 📞 Suporte

Para dúvidas ou problemas, acesse o portal de suporte:

**Portal de Suporte:** https://help.manus.im

