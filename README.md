# T2 Web - Sistema de Contratos

> Sistema completo de gerenciamento de contratos com Kanban, anexos obrigatórios e controle de permissões

## 🎯 Visão Geral

O **T2 Web** é um sistema profissional para gerenciamento do ciclo de vida de contratos imobiliários, desde a validação de dados até a assinatura final. Desenvolvido em Django com interface moderna e intuitiva.

### Principais Funcionalidades

- ✅ **Kanban Visual** com 9 fases do contrato
- ✅ **Drag & Drop** com validações e reversão automática
- ✅ **Anexos Obrigatórios** por fase (análise de crédito, vistoria, assinatura)
- ✅ **Visualizador Inline** de PDFs e imagens
- ✅ **Sistema de Permissões** com 7 grupos de usuários
- ✅ **Tela de Login Personalizada** com "Lembrar usuário"
- ✅ **Dashboard** com estatísticas e gráficos
- ✅ **Histórico Completo** de mudanças
- ✅ **Tema Profissional** preto e branco com logo T2 Web

---

## 📦 Instalação Rápida

### Requisitos
- Python 3.11+
- SQLite (incluído) ou PostgreSQL/MySQL

### Passos

```bash
# 1. Extrair projeto
unzip kanban_contratos.zip
cd kanban_contratos

# 2. Criar ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar banco
python manage.py migrate
python manage.py collectstatic --noinput

# 5. Criar superusuário
python manage.py createsuperuser

# 6. Configurar permissões
python configurar_permissoes.py

# 7. (Opcional) Popular dados de exemplo
python popular_dados.py

# 8. Iniciar servidor
python manage.py runserver
```

**Acesse**: http://localhost:8000  
**Login**: admin / sua-senha

📖 **Guia Completo**: [INICIO_RAPIDO.md](INICIO_RAPIDO.md)

---

## 🎨 Interface

### Tela de Login
- Logo T2 Web Real Estate
- Campo "Lembrar meu usuário"
- Design moderno e responsivo
- Tema preto e branco

### Kanban
- 9 colunas com cores personalizadas
- Contadores por coluna
- Drag & drop funcional
- Filtros por texto, responsável e tipo
- Badges de status e vencimento

### Formulários
- Criar/editar contratos
- Upload múltiplo de anexos
- Dropdown com tipos de documentos
- Validações em tempo real
- Detecção automática de anexos obrigatórios

---

## 📋 Fases do Contrato

1. **Validação de dados** (cinza)
2. **Análise de crédito** (laranja) - 3 anexos obrigatórios
3. **Elaboração do contrato** (mostarda)
4. **Requisição de vistoria** (teal) - 1 anexo obrigatório
5. **Minuta em aprovação** (verde)
6. **Assinatura eletrônica** (dourado) - 1 anexo obrigatório
7. **Requisição de lançamento** (roxo)
8. **Contrato assinado** (azul)
9. **Contrato cancelado** (vermelho - terminal)

---

## 📎 Anexos Obrigatórios

### Análise de Crédito (3 documentos)
1. Verificação de Processos Judiciais
2. Busca Geral de Protestos
3. Consulta de Restrições de Crédito (SPC/SERASA)

### Requisição de Vistoria (1 documento)
- Laudo de Vistoria

### Assinatura Eletrônica (1 documento)
- Contrato Assinado

**Comportamento**: Ao tentar sair da fase sem anexos, modal aparece pedindo confirmação. Digite "CONFIRMAR" para prosseguir ou clique "Voltar" para cancelar (card retorna automaticamente).

---

## 👥 Sistema de Permissões

### 7 Grupos de Usuários

1. **Administrador** - Acesso total
2. **Gerente** - Todas as fases (exceto reabrir cancelados)
3. **Analista** - Validação, elaboração, minuta
4. **Analista de Crédito** - Análise de crédito
5. **Jurídico** - Elaboração e minuta
6. **Vistoriador** - Requisição de vistoria
7. **Financeiro** - Lançamento e assinados

**Configuração**: `python configurar_permissoes.py`

---

## 🔧 Funcionalidades Detalhadas

### Gestão de Contratos
- Criar contrato (botão "Novo" no Kanban)
- Editar contrato (formulário simples, não admin)
- Visualizar detalhes completos
- Cancelar com motivo obrigatório
- Histórico de mudanças

### Sistema de Anexos
- Upload múltiplo com dropdown
- Visualizador inline (PDF/imagens)
- Download individual
- Download todos em ZIP
- Adicionar/remover no formulário de edição
- Detecção automática de tipos

### Filtros e Busca
- Busca por texto (nome, locatário, imóvel)
- Filtro por responsável
- Filtro por tipo de locatário (PF/PJ)
- Badges de garantia e vencimento

### Dashboard
- Estatísticas por status
- Contratos vencendo/vencidos
- Gráficos de distribuição
- Tabelas de ação

---

## 📚 Documentação

### Guias de Uso
- **[INICIO_RAPIDO.md](INICIO_RAPIDO.md)** - Instalação em 8 passos
- **[COMO_USAR.md](COMO_USAR.md)** - Guia completo de uso
- **[FUNCIONALIDADES_COMPLETAS.md](FUNCIONALIDADES_COMPLETAS.md)** - Detalhamento de todas as funcionalidades

### Configuração
- **[PERMISSOES.md](PERMISSOES.md)** - Sistema de permissões
- **[VSCODE_SETUP.md](VSCODE_SETUP.md)** - Configuração do VS Code
- **[ANALISE_CREDITO.md](ANALISE_CREDITO.md)** - Anexos obrigatórios

### Produção
- **[PRODUCAO.md](PRODUCAO.md)** - Guia completo de deploy em produção

---

## 🚀 Deploy em Produção

O sistema pode ser implantado em:

### Opção 1: Servidor VPS (Recomendado)
- Ubuntu + Nginx + Gunicorn + PostgreSQL
- SSL/HTTPS com Let's Encrypt
- Backup automático
- Monitoramento

### Opção 2: PythonAnywhere
- Deploy simplificado
- MySQL incluído
- HTTPS automático

### Opção 3: Heroku
- Deploy com Git
- PostgreSQL incluído
- Escalável

### Opção 4: Docker
- docker-compose.yml incluído
- PostgreSQL + Nginx
- Fácil de escalar

📖 **Guia Completo**: [PRODUCAO.md](PRODUCAO.md)

---

## 🛠️ Tecnologias

### Backend
- **Django 5.2** - Framework web
- **Python 3.11** - Linguagem
- **SQLite/PostgreSQL** - Banco de dados

### Frontend
- **Bootstrap 5** - Framework CSS
- **SortableJS** - Drag & drop
- **Bootstrap Icons** - Ícones

### Produção
- **Gunicorn** - WSGI server
- **Nginx** - Reverse proxy
- **Let's Encrypt** - SSL/TLS

---

## 📁 Estrutura do Projeto

```
kanban_contratos/
├── contratos/                 # App principal
│   ├── models.py             # Modelos (Contrato, Anexo, Histórico)
│   ├── views.py              # Views (Kanban, CRUD, Anexos)
│   ├── urls.py               # URLs do app
│   ├── admin.py              # Configuração do admin
│   ├── permissions.py        # Sistema de permissões
│   ├── middleware.py         # Middleware de login
│   ├── templates/            # Templates HTML
│   │   ├── contratos/        # Templates do app
│   │   └── registration/     # Template de login
│   └── migrations/           # Migrações do banco
├── contratos_project/        # Projeto Django
│   ├── settings.py           # Configurações
│   ├── urls.py               # URLs principais
│   └── wsgi.py               # WSGI
├── static/                   # Arquivos estáticos
│   └── img/                  # Imagens (logo)
├── templates/                # Templates globais
│   └── base.html             # Template base
├── media/                    # Uploads (criado automaticamente)
├── manage.py                 # Script Django
├── configurar_permissoes.py  # Script de permissões
├── popular_dados.py          # Script de dados de exemplo
├── requirements.txt          # Dependências Python
└── README.md                 # Este arquivo
```

---

## 🔒 Segurança

### Desenvolvimento
- SQLite local
- DEBUG=True
- SECRET_KEY padrão

### Produção
- PostgreSQL/MySQL
- DEBUG=False
- SECRET_KEY única e forte
- HTTPS obrigatório
- ALLOWED_HOSTS configurado
- CSRF/XSS protection
- Firewall configurado
- Backup automático

---

## 🐛 Solução de Problemas

### Logo não aparece
```bash
python manage.py collectstatic --noinput
# Pressione Ctrl+F5 no navegador
```

### Erro ao instalar dependências
**Windows**: Instale Visual C++ Build Tools  
**Linux**: `sudo apt-get install python3-dev`  
**Mac**: `xcode-select --install`

### Porta 8000 em uso
```bash
python manage.py runserver 8080
```

### Anexos não visualizam
- Verifique se `MEDIA_ROOT` e `MEDIA_URL` estão configurados
- Execute `python manage.py collectstatic`
- Verifique permissões da pasta `media/`

---

## 📊 Estatísticas

- **Linhas de código**: ~3.500
- **Templates**: 6
- **Models**: 3
- **Views**: 12
- **URLs**: 10
- **Migrations**: 3
- **Documentação**: 8 arquivos

---

## 🎯 Roadmap Futuro

- [ ] API REST com Django REST Framework
- [ ] Notificações por email
- [ ] Relatórios em PDF
- [ ] Integração com e-signature
- [ ] App mobile (React Native)
- [ ] Workflow customizável
- [ ] Integração com CRM

---

## 📝 Licença

© 2025 T2 Web Real Estate. Todos os direitos reservados.

---

## 🤝 Suporte

Para dúvidas ou problemas:
- Consulte a documentação completa
- Verifique o guia de solução de problemas
- Entre em contato com o suporte técnico

---

## ✅ Status do Projeto

**Versão**: 2.0  
**Status**: ✅ Produção  
**Última atualização**: Outubro 2025  
**Bugs conhecidos**: Nenhum

---

**Desenvolvido com ❤️ para T2 Web Real Estate**
#   p r o j e t o _ c o n t r a t o s  
 #   p r o j e t o _ c o n t r a t o s  
 #   p r o j e t o _ c o n t r a t o s  
 #   p r o j e t o _ c o n t r a t o s  
 #   p r o j e t o _ c o n t r a t o s  
 