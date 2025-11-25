# Sistema Kanban de Contratos T2 - Instalação Rápida

**Versão:** 2.0.0 com Tema T2 Real Estate  
**Status:** ✅ Pronto para Uso

---

## 🚀 Instalação em 5 Minutos

### 1. Instalar Dependências

```bash
cd kanban_contratos
pip install -r requirements.txt
```

### 2. Configurar Banco de Dados

```bash
python manage.py migrate
```

### 3. Criar Superusuário

```bash
python manage.py createsuperuser
```

Siga as instruções e crie:
- **Usuário:** admin (ou o que preferir)
- **Email:** seu@email.com
- **Senha:** (escolha uma senha segura)

### 4. Coletar Arquivos Estáticos

```bash
python manage.py collectstatic --noinput
```

### 5. Iniciar Servidor

```bash
python manage.py runserver
```

Acesse: **http://localhost:8000/**

---

## 🎨 Tema T2 Já Aplicado

O sistema já vem com o **tema T2 Real Estate** totalmente configurado:

- ✅ Paleta de cores oficial T2
- ✅ Logo T2 integrado
- ✅ Interface moderna e profissional
- ✅ Todas as correções implementadas

---

## 📋 Funcionalidades Incluídas

### ✅ Gestão de Contratos
- Kanban board com drag & drop
- Criação e edição de contratos
- Upload de anexos
- Visualização inline de PDFs
- Histórico de alterações

### ✅ Dashboard
- Estatísticas em tempo real
- Gráficos e métricas
- Top 10 responsáveis
- Contratos atrasados

### ✅ Sistema de Permissões
- Autenticação de usuários
- Controle de acesso
- Logs de atividades

---

## 🎯 Estrutura do Projeto

```
kanban_contratos/
├── contratos/              - App principal
│   ├── models.py          - Modelos de dados
│   ├── views.py           - Lógica de negócio
│   ├── urls.py            - Rotas
│   └── templates/         - Templates HTML
├── contratos_project/      - Configurações Django
│   └── settings.py        - Configurações
├── static/                 - Arquivos estáticos
│   ├── css/
│   │   └── t2_theme.css   - Tema T2
│   └── img/
│       └── logo.png       - Logo T2
├── templates/              - Templates base
│   └── base.html          - Template principal
├── manage.py              - Gerenciador Django
└── requirements.txt       - Dependências
```

---

## 🔧 Configurações Importantes

### Banco de Dados

Por padrão, usa **SQLite** (arquivo `db.sqlite3`).

Para usar **MySQL** em produção, veja `PRODUCAO.md`.

### Arquivos Estáticos

O tema T2 está em `/static/css/t2_theme.css`.

Para modificar cores, edite as variáveis CSS:

```css
:root {
    --t2-azul: #5B7FDB;
    --t2-verde: #5EADA5;
    --t2-amarelo: #F5B85F;
    --t2-laranja: #F58B5F;
}
```

### Segurança

**IMPORTANTE:** Antes de colocar em produção:

1. Altere `SECRET_KEY` em `settings.py`
2. Configure `DEBUG = False`
3. Adicione seu domínio em `ALLOWED_HOSTS`
4. Configure HTTPS

---

## 📖 Documentação Completa

- **`PRODUCAO.md`** - Deploy em produção
- **`FUNCIONALIDADES.md`** - Lista de funcionalidades
- **`PERMISSOES.md`** - Sistema de permissões

---

## 🐛 Solução de Problemas

### Erro ao migrar banco de dados

```bash
python manage.py migrate --run-syncdb
```

### CSS não está sendo aplicado

```bash
python manage.py collectstatic --clear --noinput
```

### Erro de permissão em arquivos

```bash
chmod -R 755 static/
chmod -R 755 media/
```

---

## 📞 Suporte

Para dúvidas ou problemas:

**Portal de Suporte:** https://help.manus.im

---

## ✅ Checklist de Instalação

- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Banco de dados migrado (`python manage.py migrate`)
- [ ] Superusuário criado (`python manage.py createsuperuser`)
- [ ] Arquivos estáticos coletados (`collectstatic`)
- [ ] Servidor iniciado (`runserver`)
- [ ] Login realizado com sucesso
- [ ] Tema T2 visível na interface

---

**Pronto! Seu sistema está funcionando com o tema T2 Real Estate!** 🎉
