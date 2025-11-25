# T2 Web - Início Rápido

> Instale e execute o sistema em **5 minutos**!

## ⚡ Instalação Rápida

### Passo 1: Extrair Projeto

```bash
# Extrair ZIP
unzip kanban_contratos.zip
cd kanban_contratos

# Ou extrair TAR.GZ
tar -xzf kanban_contratos.tar.gz
cd kanban_contratos
```

### Passo 2: Criar Ambiente Virtual

**Windows**:
```bash
python -m venv venv
.\venv\Scripts\activate
```

**Mac/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Passo 3: Instalar Dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar Banco de Dados

```bash
# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos (logo)
python manage.py collectstatic --noinput

# Criar superusuário
python manage.py createsuperuser
```

**Dados sugeridos**:
- Username: `admin`
- Email: `admin@t2web.com`
- Password: `admin123`

### Passo 5: Configurar Permissões

```bash
python configurar_permissoes.py
```

### Passo 6 (Opcional): Popular Dados

```bash
python popular_dados.py
```

### Passo 7: Iniciar Servidor

```bash
python manage.py runserver
```

### Passo 8: Acessar

**URL**: http://localhost:8000  
**Login**: admin / admin123

---

## 🎯 Pronto!

Sistema funcionando com:
- ✅ Logo T2 Web
- ✅ Kanban com 9 colunas
- ✅ Drag & drop
- ✅ Anexos obrigatórios

---

## 📚 Documentação

- [README.md](README.md) - Visão geral
- [COMO_USAR.md](COMO_USAR.md) - Guia de uso
- [PERMISSOES.md](PERMISSOES.md) - Permissões
- [ANALISE_CREDITO.md](ANALISE_CREDITO.md) - Anexos

**Divirta-se! 🚀**
