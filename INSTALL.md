# Guia Rápido de Instalação

## ⚡ Instalação Rápida (Ubuntu/Debian)

### 1. Instalar Dependências do Sistema

```bash
sudo apt-get update
sudo apt-get install -y mysql-server default-libmysqlclient-dev pkg-config build-essential python3.11-dev python3-pip
```

### 2. Configurar MySQL

```bash
# Iniciar MySQL
sudo service mysql start

# Criar banco de dados
sudo mysql -e "CREATE DATABASE contratos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'contratos_user'@'localhost' IDENTIFIED BY 'contratos_pass';"
sudo mysql -e "GRANT ALL PRIVILEGES ON contratos_db.* TO 'contratos_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### 3. Instalar Dependências Python

```bash
cd kanban_contratos
pip3 install -r requirements.txt
```

### 4. Configurar Django

```bash
# Executar migrações
python3.11 manage.py makemigrations
python3.11 manage.py migrate

# Criar superusuário
python3.11 manage.py createsuperuser
# Usuário sugerido: admin
# Senha sugerida: admin123

# (Opcional) Popular com dados de exemplo
python3.11 popular_dados.py
```

### 5. Iniciar Servidor

```bash
python3.11 manage.py runserver 0.0.0.0:8000
```

### 6. Acessar o Sistema

Abra o navegador e acesse:
- **Sistema**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Kanban**: http://localhost:8000/kanban
- **Dashboard**: http://localhost:8000/kanban/dashboard

---

## 🐳 Instalação com Docker (Alternativa)

### Criar Dockerfile

```dockerfile
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    pkg-config \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Configurar diretório de trabalho
WORKDIR /app

# Copiar e instalar dependências Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do projeto
COPY . .

# Expor porta
EXPOSE 8000

# Comando de inicialização
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### Criar docker-compose.yml

```yaml
version: '3.8'

services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: contratos_db
      MYSQL_USER: contratos_user
      MYSQL_PASSWORD: contratos_pass
      MYSQL_ROOT_PASSWORD: root_pass
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  web:
    build: .
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DB_HOST: db
      DB_NAME: contratos_db
      DB_USER: contratos_user
      DB_PASSWORD: contratos_pass

volumes:
  mysql_data:
```

### Executar com Docker

```bash
# Construir e iniciar containers
docker-compose up -d

# Executar migrações
docker-compose exec web python manage.py migrate

# Criar superusuário
docker-compose exec web python manage.py createsuperuser

# Popular dados de exemplo
docker-compose exec web python popular_dados.py
```

---

## 🔧 Configuração de Produção

### 1. Configurar Variáveis de Ambiente

```bash
# Copiar arquivo de exemplo
cp .env.example .env

# Editar com suas configurações
nano .env
```

### 2. Ajustar settings.py para Produção

```python
# Em contratos_project/settings.py

DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com', 'www.seu-dominio.com']

# Usar variáveis de ambiente
import os
from pathlib import Path

SECRET_KEY = os.environ.get('SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}
```

### 3. Coletar Arquivos Estáticos

```bash
python3.11 manage.py collectstatic --noinput
```

### 4. Configurar Nginx (exemplo)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location /static/ {
        alias /caminho/para/kanban_contratos/staticfiles/;
    }

    location /media/ {
        alias /caminho/para/kanban_contratos/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. Configurar Gunicorn

```bash
# Instalar Gunicorn
pip3 install gunicorn

# Executar
gunicorn contratos_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## ✅ Verificação da Instalação

Execute os seguintes comandos para verificar se tudo está funcionando:

```bash
# Verificar se MySQL está rodando
sudo service mysql status

# Verificar se o banco foi criado
mysql -u contratos_user -pcontratos_pass -e "SHOW DATABASES;"

# Verificar migrações
python3.11 manage.py showmigrations

# Verificar se o servidor inicia
python3.11 manage.py check
```

---

## 🐛 Problemas Comuns

### Erro: "Access denied for user"
```bash
# Recriar usuário MySQL
sudo mysql -e "DROP USER IF EXISTS 'contratos_user'@'localhost';"
sudo mysql -e "CREATE USER 'contratos_user'@'localhost' IDENTIFIED BY 'contratos_pass';"
sudo mysql -e "GRANT ALL PRIVILEGES ON contratos_db.* TO 'contratos_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### Erro: "mysqlclient not found"
```bash
# Instalar dependências de desenvolvimento
sudo apt-get install -y default-libmysqlclient-dev pkg-config build-essential python3.11-dev
pip3 install mysqlclient
```

### Erro: "Port 8000 already in use"
```bash
# Encontrar processo usando a porta
sudo lsof -i :8000

# Matar processo
kill -9 <PID>

# Ou usar outra porta
python3.11 manage.py runserver 0.0.0.0:8001
```

---

## 📞 Suporte

Se você encontrar problemas durante a instalação:

1. Verifique os logs do Django
2. Verifique os logs do MySQL: `sudo tail -f /var/log/mysql/error.log`
3. Consulte a documentação completa no README.md
