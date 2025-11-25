# Instalação Simplificada com SQLite

Este guia mostra como instalar o sistema **sem precisar do MySQL**, usando SQLite que já vem com o Python!

## ✨ Por que SQLite?

- ✅ **Sem instalação** - Já vem com o Python
- ✅ **Sem configuração** - Não precisa criar usuários ou bancos
- ✅ **Arquivo único** - Todo o banco em um arquivo db.sqlite3
- ✅ **Perfeito para desenvolvimento** - Rápido e simples
- ✅ **Funciona em qualquer OS** - Windows, Mac, Linux

## 📋 Pré-requisitos

Você só precisa de:
- **Python 3.11 ou superior** - [Download aqui](https://www.python.org/downloads/)
- **Visual Studio Code** (opcional) - [Download aqui](https://code.visualstudio.com/)

**Não precisa de MySQL!** 🎉

---

## 🚀 Instalação Rápida

### Passo 1: Extrair o Projeto

Extraia o arquivo `kanban_contratos.zip` em uma pasta de sua escolha.

### Passo 2: Configurar para SQLite

**Opção A - Renomear arquivo (mais simples)**

```bash
# No Windows (PowerShell)
cd kanban_contratos
Rename-Item contratos_project\settings.py contratos_project\settings_mysql.py
Rename-Item contratos_project\settings_sqlite.py contratos_project\settings.py

# No Mac/Linux
cd kanban_contratos
mv contratos_project/settings.py contratos_project/settings_mysql.py
mv contratos_project/settings_sqlite.py contratos_project/settings.py
```

**Opção B - Variável de ambiente**

```bash
# Definir variável de ambiente
set DJANGO_SETTINGS_MODULE=contratos_project.settings_sqlite  # Windows
export DJANGO_SETTINGS_MODULE=contratos_project.settings_sqlite  # Mac/Linux
```

### Passo 3: Criar Ambiente Virtual

**No Windows:**
```powershell
cd kanban_contratos
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements_sqlite.txt
```

**No Mac/Linux:**
```bash
cd kanban_contratos
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_sqlite.txt
```

### Passo 4: Configurar Banco de Dados

```bash
# Criar tabelas
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
# Usuário: admin
# Email: admin@example.com
# Senha: admin123

# (Opcional) Popular com dados de exemplo
python popular_dados.py
```

### Passo 5: Iniciar o Servidor

```bash
python manage.py runserver
```

Pronto! Acesse http://localhost:8000 🎉

---

## 💻 Instalação no VS Code

### 1. Abrir Projeto

1. Abra o VS Code
2. File → Open Folder
3. Selecione a pasta `kanban_contratos`

### 2. Instalar Extensão Python

1. Pressione **Ctrl+Shift+X**
2. Busque por "Python"
3. Instale a extensão da Microsoft

### 3. Selecionar Interpretador

1. Pressione **Ctrl+Shift+P**
2. Digite: "Python: Select Interpreter"
3. Escolha o Python do ambiente virtual (`./venv/Scripts/python.exe`)

### 4. Configurar para SQLite

Siga o **Passo 2** da instalação rápida acima.

### 5. Abrir Terminal Integrado

1. Pressione **Ctrl+`** (ou View → Terminal)
2. O ambiente virtual deve ativar automaticamente
3. Se não ativar, execute:
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`

### 6. Instalar Dependências

```bash
pip install -r requirements_sqlite.txt
```

### 7. Configurar Banco de Dados

```bash
python manage.py migrate
python manage.py createsuperuser
python popular_dados.py  # Opcional
```

### 8. Iniciar com Debug

Pressione **F5** e o servidor iniciará automaticamente!

Ou no terminal:
```bash
python manage.py runserver
```

---

## 📊 Comparação: SQLite vs MySQL

| Característica | SQLite | MySQL |
|----------------|--------|-------|
| **Instalação** | ✅ Nenhuma | ❌ Requer instalação |
| **Configuração** | ✅ Automática | ❌ Criar DB e usuário |
| **Arquivo** | ✅ Único arquivo | ❌ Servidor separado |
| **Performance** | ✅ Rápido para dev | ✅ Melhor para produção |
| **Backup** | ✅ Copiar arquivo | ❌ Comando mysqldump |
| **Multi-usuário** | ⚠️ Limitado | ✅ Excelente |
| **Tamanho máximo** | ⚠️ ~140 TB | ✅ Praticamente ilimitado |

### Quando usar cada um?

**Use SQLite se:**
- ✅ Está desenvolvendo/testando
- ✅ Quer começar rápido
- ✅ Tem poucos usuários simultâneos
- ✅ Não quer instalar MySQL

**Use MySQL se:**
- ✅ Está em produção
- ✅ Tem muitos usuários simultâneos
- ✅ Precisa de recursos avançados
- ✅ Já tem MySQL instalado

---

## 🔄 Migrar de SQLite para MySQL depois

Se quiser migrar para MySQL no futuro:

### 1. Exportar dados do SQLite

```bash
python manage.py dumpdata > backup.json
```

### 2. Configurar MySQL

Siga as instruções do `INSTALL.md`

### 3. Trocar configuração

```bash
# Renomear de volta
mv contratos_project/settings.py contratos_project/settings_sqlite.py
mv contratos_project/settings_mysql.py contratos_project/settings.py
```

### 4. Criar tabelas no MySQL

```bash
pip install mysqlclient
python manage.py migrate
```

### 5. Importar dados

```bash
python manage.py loaddata backup.json
```

Pronto! Seus dados foram migrados para MySQL.

---

## 🗂️ Estrutura de Arquivos SQLite

Após a instalação, você terá:

```
kanban_contratos/
├── db.sqlite3              ← Seu banco de dados (arquivo único)
├── venv/                   ← Ambiente virtual Python
├── contratos/              ← App Django
├── manage.py               ← Gerenciador Django
└── requirements_sqlite.txt ← Dependências (sem MySQL)
```

O arquivo `db.sqlite3` contém todo o banco de dados. Para fazer backup, basta copiar este arquivo!

---

## 🛠️ Comandos Úteis

### Ver dados no SQLite

**Opção 1 - Django Admin**
```bash
python manage.py runserver
# Acesse http://localhost:8000/admin
```

**Opção 2 - Django Shell**
```bash
python manage.py shell
>>> from contratos.models import Contrato
>>> Contrato.objects.all()
```

**Opção 3 - SQLite Browser**
- Baixe [DB Browser for SQLite](https://sqlitebrowser.org/)
- Abra o arquivo `db.sqlite3`

### Resetar banco de dados

```bash
# Apagar banco
rm db.sqlite3  # Mac/Linux
del db.sqlite3  # Windows

# Recriar
python manage.py migrate
python manage.py createsuperuser
python popular_dados.py
```

### Fazer backup

```bash
# Copiar arquivo
cp db.sqlite3 db.backup.sqlite3  # Mac/Linux
copy db.sqlite3 db.backup.sqlite3  # Windows

# Ou exportar para JSON
python manage.py dumpdata > backup.json
```

---

## 🐛 Solução de Problemas

### Erro: "no such table"

```bash
# Executar migrações
python manage.py migrate
```

### Erro: "database is locked"

O SQLite permite apenas uma escrita por vez. Se isso acontecer:
1. Feche todos os programas acessando o banco
2. Reinicie o servidor Django

### Erro: "unable to open database file"

Verifique se você está na pasta correta:
```bash
cd kanban_contratos
python manage.py runserver
```

### Banco de dados corrompido

```bash
# Recriar do zero
rm db.sqlite3
python manage.py migrate
python popular_dados.py
```

---

## 📝 Diferenças no Código

O sistema funciona **exatamente igual** com SQLite ou MySQL. A única diferença é a configuração em `settings.py`:

**SQLite:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**MySQL:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'contratos_db',
        'USER': 'contratos_user',
        'PASSWORD': 'contratos_pass',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

Todo o resto do código é idêntico!

---

## ✅ Checklist de Instalação

- [ ] Python 3.11+ instalado
- [ ] Projeto extraído
- [ ] Configurado para usar SQLite (renomeado settings)
- [ ] Ambiente virtual criado
- [ ] Dependências instaladas (`requirements_sqlite.txt`)
- [ ] Migrações executadas
- [ ] Superusuário criado
- [ ] Dados de exemplo populados (opcional)
- [ ] Servidor rodando
- [ ] Sistema acessível no navegador

---

## 🎉 Pronto!

Agora você tem o sistema rodando **sem precisar instalar MySQL**!

- **Kanban**: http://localhost:8000/kanban
- **Dashboard**: http://localhost:8000/kanban/dashboard
- **Admin**: http://localhost:8000/admin

**Login**: admin / admin123

Se tiver dúvidas, consulte:
- `README.md` - Documentação completa
- `VSCODE_SETUP.md` - Configuração do VS Code
- `INSTALL.md` - Instalação com MySQL (se quiser migrar depois)

---

**Desenvolvido com Django + SQLite + Bootstrap 5**
