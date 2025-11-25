# Guia de Instalação no VS Code

Este guia mostra como instalar e executar o Sistema de Contratos Kanban no Visual Studio Code.

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

1. **Visual Studio Code** - [Download aqui](https://code.visualstudio.com/)
2. **Python 3.11 ou superior** - [Download aqui](https://www.python.org/downloads/)
3. **Git** (opcional) - [Download aqui](https://git-scm.com/downloads)

**Não precisa de MySQL!** O sistema usa SQLite que já vem com o Python. ✅

## 🔌 Extensões Recomendadas para VS Code

Abra o VS Code e instale estas extensões (Ctrl+Shift+X):

### Essenciais
- **Python** (Microsoft) - ID: ms-python.python
- **Pylance** (Microsoft) - ID: ms-python.vscode-pylance

### Recomendadas
- **Django** (Baptiste Darthenay) - ID: batisteo.vscode-django
- **HTML CSS Support** - ID: ecmel.vscode-html-css
- **Bootstrap 5 Quick Snippets** - ID: anbuselvanrocky.bootstrap5-vscode
- **Better Comments** - ID: aaron-bond.better-comments
- **GitLens** (se usar Git) - ID: eamodio.gitlens

## 📦 Passo 1: Extrair o Projeto

1. Extraia o arquivo `kanban_contratos.zip` em uma pasta de sua escolha
2. Abra o VS Code
3. Vá em **File → Open Folder** (ou Ctrl+K Ctrl+O)
4. Selecione a pasta `kanban_contratos`

## 🐍 Passo 2: Configurar Ambiente Virtual Python

### No Windows

Abra o terminal integrado do VS Code (Ctrl+` ou View → Terminal) e execute:

```powershell
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
.\venv\Scripts\activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### No macOS/Linux

```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

**Dica**: O VS Code detectará automaticamente o ambiente virtual e perguntará se deseja usá-lo. Clique em "Yes".

## ⚙️ Passo 3: Configurar o Django

**Boa notícia:** O sistema já está configurado para usar SQLite! Não precisa configurar banco de dados manualmente. 🎉

No terminal do VS Code (com ambiente virtual ativado):

```bash
# Executar migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

Quando solicitado, preencha:
- **Username**: admin
- **Email**: admin@example.com
- **Password**: admin123 (ou sua preferência)
- **Password (again)**: admin123

### (Opcional) Popular com Dados de Exemplo

```bash
python popular_dados.py
```

Isso criará 33 contratos de exemplo para você testar o sistema.

## 🚀 Passo 4: Executar o Servidor

No terminal do VS Code:

```bash
python manage.py runserver
```

Você verá algo como:

```
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

Agora abra seu navegador e acesse:
- **Sistema**: http://localhost:8000
- **Admin**: http://localhost:8000/admin
- **Kanban**: http://localhost:8000/kanban

## 🔧 Configuração do VS Code

### 1. Configurar Python Interpreter

1. Pressione **Ctrl+Shift+P**
2. Digite: "Python: Select Interpreter"
3. Selecione o interpretador do ambiente virtual (`./venv/Scripts/python.exe` no Windows ou `./venv/bin/python` no Linux/Mac)

### 2. Criar Configuração de Debug

Crie o arquivo `.vscode/launch.json` na raiz do projeto:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Django: Run Server",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "0.0.0.0:8000"
            ],
            "django": true,
            "justMyCode": true
        },
        {
            "name": "Django: Run Tests",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "test"
            ],
            "django": true,
            "justMyCode": true
        }
    ]
}
```

Agora você pode iniciar o servidor com debug pressionando **F5**.

### 3. Configurar Settings do VS Code

Crie o arquivo `.vscode/settings.json`:

```json
{
    "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "autopep8",
    "python.analysis.typeCheckingMode": "basic",
    "files.associations": {
        "**/*.html": "html",
        "**/templates/**/*.html": "django-html",
        "**/templates/**/*": "django-txt",
        "**/requirements{/**,*}.{txt,in}": "pip-requirements"
    },
    "emmet.includeLanguages": {
        "django-html": "html"
    },
    "[python]": {
        "editor.formatOnSave": true,
        "editor.codeActionsOnSave": {
            "source.organizeImports": true
        }
    },
    "files.exclude": {
        "**/__pycache__": true,
        "**/*.pyc": true
    }
}
```

### 4. Criar Tasks para Comandos Comuns

Crie o arquivo `.vscode/tasks.json`:

```json
{
    "version": "2.0.0",
    "tasks": [
        {
            "label": "Django: Run Server",
            "type": "shell",
            "command": "${config:python.defaultInterpreterPath}",
            "args": ["manage.py", "runserver"],
            "problemMatcher": [],
            "group": {
                "kind": "build",
                "isDefault": true
            }
        },
        {
            "label": "Django: Make Migrations",
            "type": "shell",
            "command": "${config:python.defaultInterpreterPath}",
            "args": ["manage.py", "makemigrations"],
            "problemMatcher": []
        },
        {
            "label": "Django: Migrate",
            "type": "shell",
            "command": "${config:python.defaultInterpreterPath}",
            "args": ["manage.py", "migrate"],
            "problemMatcher": []
        },
        {
            "label": "Django: Create Superuser",
            "type": "shell",
            "command": "${config:python.defaultInterpreterPath}",
            "args": ["manage.py", "createsuperuser"],
            "problemMatcher": []
        }
    ]
}
```

Agora você pode executar tarefas com **Ctrl+Shift+B**.

## 🎯 Atalhos Úteis no VS Code

### Navegação
- **Ctrl+P** - Buscar arquivo
- **Ctrl+Shift+F** - Buscar em todos os arquivos
- **Ctrl+G** - Ir para linha
- **F12** - Ir para definição
- **Alt+←/→** - Voltar/Avançar na navegação

### Edição
- **Ctrl+D** - Selecionar próxima ocorrência
- **Ctrl+Shift+L** - Selecionar todas as ocorrências
- **Alt+↑/↓** - Mover linha
- **Ctrl+/** - Comentar/descomentar

### Terminal
- **Ctrl+`** - Abrir/fechar terminal
- **Ctrl+Shift+`** - Novo terminal

### Debug
- **F5** - Iniciar debug
- **F9** - Toggle breakpoint
- **F10** - Step over
- **F11** - Step into

## 📁 Estrutura do Projeto no VS Code

```
kanban_contratos/
├── .vscode/                    # Configurações do VS Code
│   ├── launch.json            # Configuração de debug
│   ├── settings.json          # Configurações do projeto
│   └── tasks.json             # Tarefas automatizadas
├── venv/                      # Ambiente virtual Python
├── contratos/                 # App Django principal
│   ├── migrations/            # Migrações do banco
│   ├── templates/             # Templates HTML
│   ├── models.py              # Modelos de dados
│   ├── views.py               # Lógica de negócio
│   ├── admin.py               # Interface admin
│   └── urls.py                # Rotas do app
├── contratos_project/         # Configurações do projeto
│   ├── settings.py            # Configurações Django
│   └── urls.py                # Rotas principais
├── templates/                 # Templates globais
├── static/                    # Arquivos estáticos
├── media/                     # Uploads
├── manage.py                  # Gerenciador Django
├── requirements.txt           # Dependências
└── README.md                  # Documentação
```

## 🐛 Solução de Problemas no VS Code

### Python não encontrado

Se o VS Code não encontrar o Python:
1. Pressione **Ctrl+Shift+P**
2. Digite "Python: Select Interpreter"
3. Escolha o Python instalado ou o do ambiente virtual

### Ambiente virtual não ativa automaticamente

Adicione ao `.vscode/settings.json`:
```json
{
    "python.terminal.activateEnvironment": true
}
```

### Intellisense não funciona

1. Certifique-se de que o Pylance está instalado
2. Verifique se o interpretador correto está selecionado
3. Recarregue a janela: **Ctrl+Shift+P** → "Developer: Reload Window"

### Erro "no such table"

Se aparecer erro de tabela não encontrada:

```bash
python manage.py migrate
```

### Banco de dados travado (database is locked)

O SQLite permite apenas uma escrita por vez. Se isso acontecer:
1. Feche outros programas acessando o banco
2. Reinicie o servidor Django

## 🎨 Temas Recomendados

Para uma melhor experiência visual:

- **One Dark Pro** - Tema escuro popular
- **Material Theme** - Tema moderno e colorido
- **Dracula Official** - Tema escuro elegante
- **GitHub Theme** - Tema claro/escuro do GitHub

Instale via **Ctrl+Shift+X** e busque por "theme".

## 📚 Recursos Adicionais

### Documentação
- [Django Documentation](https://docs.djangoproject.com/)
- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Django Tutorial](https://code.visualstudio.com/docs/python/tutorial-django)

### Snippets Úteis

Crie snippets personalizados em **File → Preferences → User Snippets → python.json**:

```json
{
    "Django Model": {
        "prefix": "djmodel",
        "body": [
            "class ${1:ModelName}(models.Model):",
            "    ${2:field_name} = models.${3:CharField}(${4:max_length=100})",
            "    created_at = models.DateTimeField(auto_now_add=True)",
            "    updated_at = models.DateTimeField(auto_now=True)",
            "",
            "    class Meta:",
            "        verbose_name = '${5:Model Name}'",
            "        verbose_name_plural = '${6:Model Names}'",
            "",
            "    def __str__(self):",
            "        return self.${7:field_name}"
        ]
    }
}
```

## ✅ Checklist de Instalação

Marque conforme for completando:

- [ ] VS Code instalado
- [ ] Python 3.11+ instalado
- [ ] Extensões do VS Code instaladas (Python + Pylance)
- [ ] Projeto extraído e aberto no VS Code
- [ ] Ambiente virtual criado e ativado
- [ ] Dependências instaladas (requirements.txt)
- [ ] Migrações executadas (migrate)
- [ ] Superusuário criado (createsuperuser)
- [ ] Dados de exemplo populados (opcional)
- [ ] Servidor rodando com sucesso
- [ ] Sistema acessível no navegador

## 🎉 Pronto!

Agora você tem um ambiente de desenvolvimento completo no VS Code para trabalhar com o Sistema de Contratos Kanban!

Para iniciar o desenvolvimento:
1. Abra o terminal integrado (**Ctrl+`**)
2. Ative o ambiente virtual (se não estiver ativo)
3. Execute `python manage.py runserver`
4. Acesse http://localhost:8000

**Dica**: Use o debug do VS Code (**F5**) para depurar o código com breakpoints!

---

**Dúvidas?** Consulte a documentação completa no README.md
