# Sistema de Acompanhamento de Contratos - Kanban

Sistema completo de gestão de contratos de locação com visualização Kanban, desenvolvido em Django e MySQL.

## 📋 Características Principais

### ✅ Funcionalidades Implementadas

- **Visualização Kanban Completa**
  - 9 colunas de status na ordem especificada
  - Drag & drop funcional para mudança de status
  - Contadores de cards por coluna
  - Cores personalizadas por status
  - Scroll horizontal responsivo

- **Gestão de Contratos**
  - CRUD completo via Django Admin
  - Campos completos: locatário, imóvel, vigência, garantia, responsável
  - Controle de SLA por fase
  - Histórico automático de mudanças de status
  - Sistema de anexos

- **Filtros Avançados**
  - Busca por texto (nome, locatário, imóvel)
  - Filtro por responsável
  - Filtro por tipo de locatário (PF/PJ)

- **Badges e Indicadores**
  - Badge de tipo de garantia
  - Badge de vencimento (verde/amarelo/vermelho)
  - Badge de SLA excedido
  - Indicador de anexos presentes

- **Validações e Regras de Negócio**
  - Motivo obrigatório ao cancelar contrato
  - Apenas admin pode reabrir contratos cancelados
  - Validação de status válidos
  - Atualização automática de data de entrada na fase

- **Dashboard de Estatísticas**
  - Total de contratos
  - Contratos com SLA excedido
  - Distribuição por status
  - Top 10 responsáveis
  - Lista detalhada de contratos atrasados

- **Página de Detalhes**
  - Informações completas do contrato
  - Histórico de mudanças de status
  - Lista de anexos
  - Ações rápidas (editar, voltar ao Kanban)

## 🚀 Tecnologias Utilizadas

- **Backend**: Django 5.2.7
- **Banco de Dados**: MySQL 8.0
- **Frontend**: Bootstrap 5.3.0, SortableJS 1.15.0
- **Linguagem**: Python 3.11

## 📦 Estrutura do Projeto

```
kanban_contratos/
├── contratos/                      # App principal
│   ├── models.py                   # Modelos (Contrato, AnexoContrato, HistoricoStatus)
│   ├── views.py                    # Views (kanban, mudar_status, detalhe, dashboard)
│   ├── admin.py                    # Configuração do Django Admin
│   ├── urls.py                     # URLs do app
│   └── templates/contratos/        # Templates
│       ├── kanban.html             # Visualização Kanban
│       ├── detalhe.html            # Detalhes do contrato
│       └── dashboard.html          # Dashboard de estatísticas
├── contratos_project/              # Configurações do projeto
│   ├── settings.py                 # Configurações Django
│   └── urls.py                     # URLs principais
├── templates/                      # Templates globais
│   └── base.html                   # Template base
├── static/                         # Arquivos estáticos
├── media/                          # Uploads de arquivos
├── popular_dados.py                # Script para popular banco com dados de exemplo
├── manage.py                       # Gerenciador Django
└── README.md                       # Este arquivo
```

## 🔧 Instalação e Configuração

### Pré-requisitos

- Python 3.11
- MySQL 8.0
- pip

### Passo 1: Instalar Dependências do Sistema

```bash
sudo apt-get update
sudo apt-get install -y mysql-server default-libmysqlclient-dev pkg-config build-essential python3.11-dev
```

### Passo 2: Configurar MySQL

```bash
# Iniciar MySQL
sudo service mysql start

# Criar banco de dados e usuário
sudo mysql -e "CREATE DATABASE contratos_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
sudo mysql -e "CREATE USER 'contratos_user'@'localhost' IDENTIFIED BY 'contratos_pass';"
sudo mysql -e "GRANT ALL PRIVILEGES ON contratos_db.* TO 'contratos_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### Passo 3: Instalar Dependências Python

```bash
cd kanban_contratos
pip3 install django mysqlclient pillow
```

### Passo 4: Executar Migrações

```bash
python3.11 manage.py makemigrations
python3.11 manage.py migrate
```

### Passo 5: Criar Superusuário

```bash
python3.11 manage.py createsuperuser
# Usuário: admin
# Email: admin@example.com
# Senha: admin123 (ou sua preferência)
```

### Passo 6: Popular Banco de Dados (Opcional)

```bash
python3.11 popular_dados.py
```

Este script cria:
- 4 usuários de exemplo (joao.silva, maria.santos, carlos.oliveira, ana.costa)
- 30 contratos distribuídos em diferentes status
- 3 contratos cancelados
- Alguns contratos com SLA excedido para demonstração

### Passo 7: Iniciar Servidor

```bash
python3.11 manage.py runserver 0.0.0.0:8000
```

Acesse: http://localhost:8000

## 📖 Guia de Uso

### Acessando o Sistema

1. **Login**: Acesse http://localhost:8000 e faça login com suas credenciais
2. **Kanban**: Visualização principal com todos os contratos organizados por status
3. **Dashboard**: Estatísticas e contratos com SLA excedido
4. **Admin**: Gerenciamento completo de contratos, usuários e dados

### Usando o Kanban

#### Visualizar Contratos
- Cada card mostra: nome da negociação, locatário, imóvel, vencimento, responsável
- Badges coloridos indicam: garantia, dias para vencimento, SLA excedido, anexos

#### Mover Contratos (Drag & Drop)
1. Clique e segure um card
2. Arraste para a coluna desejada
3. Solte o card na nova coluna
4. O status será atualizado automaticamente

**Observação**: Ao mover para "Contrato cancelado", será solicitado o motivo do cancelamento.

#### Filtrar Contratos
- **Busca por texto**: Digite nome do contrato, locatário ou endereço
- **Filtro por responsável**: Selecione um usuário específico
- **Filtro por tipo**: Escolha entre Pessoa Física ou Pessoa Jurídica

#### Ver Detalhes
- Clique no botão "Ver detalhes" em qualquer card
- Visualize todas as informações do contrato
- Acesse o histórico de mudanças de status
- Veja e baixe anexos

### Gerenciando Contratos no Admin

1. Acesse http://localhost:8000/admin/
2. Navegue até "Contratos" > "Contratos"
3. Adicione, edite ou visualize contratos
4. Configure SLA, anexos e outras informações

### Dashboard de Estatísticas

O dashboard mostra:
- **Total de contratos** no sistema
- **Contratos atrasados** (SLA excedido)
- **Taxa de sucesso** (contratos dentro do prazo)
- **Distribuição por status** com percentuais
- **Top 10 responsáveis** por número de contratos
- **Lista detalhada** de contratos com SLA excedido

## 🎨 Cores das Colunas

| Status | Cor | Hex |
|--------|-----|-----|
| Validação de dados | Cinza | #6c757d |
| Análise de crédito | Laranja | #fd7e14 |
| Elaboração do contrato | Mostarda | #ffc107 |
| Requisição de vistoria | Teal | #20c997 |
| Minuta em aprovação | Verde | #28a745 |
| Assinatura eletrônica | Dourado | #ffc107 |
| Requisição de lançamento | Roxo | #6f42c1 |
| Contrato assinado | Azul | #007bff |
| Contrato cancelado | Vermelho | #dc3545 |

## 📊 Modelos de Dados

### Contrato
- **Identificação**: nome_negociacao, status
- **Locatário**: nome, tipo (PF/PJ), documento
- **Imóvel**: endereco, codigo
- **Vigência**: inicio_vigencia, fim_vigencia, valor_aluguel
- **Garantia**: tipo_garantia
- **Controle**: responsavel, data_entrada_fase, prazo_fase_dias
- **Cancelamento**: motivo_cancelamento
- **Anexos**: possui_anexos
- **Auditoria**: criado_em, atualizado_em

### AnexoContrato
- **Arquivo**: arquivo (upload)
- **Metadados**: descricao, enviado_em, enviado_por
- **Relacionamento**: contrato (ForeignKey)

### HistoricoStatus
- **Mudança**: status_anterior, status_novo
- **Auditoria**: alterado_por, alterado_em, observacao
- **Relacionamento**: contrato (ForeignKey)

## 🔒 Regras de Negócio

### Mudança de Status
- ✅ Livre entre todas as colunas (exceto cancelado)
- ✅ Motivo obrigatório ao cancelar
- ✅ Apenas admin pode reabrir contratos cancelados
- ✅ Histórico automático de todas as mudanças
- ✅ Atualização automática da data de entrada na fase

### SLA (Service Level Agreement)
- Cada contrato tem um prazo esperado para a fase atual
- Sistema calcula automaticamente dias na fase
- Badge vermelho indica SLA excedido
- Dashboard lista todos os contratos atrasados

### Vencimento de Contratos
- **Verde**: Mais de 30 dias para vencer
- **Amarelo**: 30 dias ou menos para vencer
- **Vermelho**: Vencido

## 🛠️ Personalização

### Alterar Prazo Padrão de SLA
Edite em `contratos/models.py`:
```python
prazo_fase_dias = models.IntegerField(
    default=5,  # Altere este valor
    ...
)
```

### Adicionar Novos Status
1. Edite `STATUS_CHOICES` em `contratos/models.py`
2. Adicione cor em `cor_coluna_status()`
3. Execute `python3.11 manage.py makemigrations`
4. Execute `python3.11 manage.py migrate`

### Personalizar Cores
Edite as cores no método `cor_coluna_status()` em `contratos/models.py`

## 📝 Credenciais de Acesso (Dados de Exemplo)

### Admin
- **Usuário**: admin
- **Senha**: admin123

### Usuários de Exemplo
- **joao.silva** / senha123
- **maria.santos** / senha123
- **carlos.oliveira** / senha123
- **ana.costa** / senha123

## 🐛 Solução de Problemas

### Erro de Conexão com MySQL
```bash
# Verificar se MySQL está rodando
sudo service mysql status

# Reiniciar MySQL
sudo service mysql restart
```

### Erro de Permissões
```bash
# Recriar permissões do banco
sudo mysql -e "GRANT ALL PRIVILEGES ON contratos_db.* TO 'contratos_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"
```

### Erro de Migrações
```bash
# Resetar migrações (CUIDADO: apaga dados)
python3.11 manage.py migrate contratos zero
python3.11 manage.py migrate
```

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais e de demonstração.

## 👥 Suporte

Para dúvidas ou problemas:
1. Verifique a documentação acima
2. Consulte os logs do Django
3. Verifique o console do navegador para erros de JavaScript

## 🎯 Próximos Passos (Sugestões)

- [ ] Implementar notificações por email para SLA excedido
- [ ] Adicionar relatórios em PDF
- [ ] Implementar API REST
- [ ] Adicionar autenticação via OAuth
- [ ] Implementar sistema de permissões granulares
- [ ] Adicionar gráficos interativos no dashboard
- [ ] Implementar busca avançada com mais filtros
- [ ] Adicionar exportação de dados para Excel
- [ ] Implementar sistema de comentários nos contratos
- [ ] Adicionar notificações em tempo real (WebSockets)

---

**Desenvolvido com Django + MySQL + Bootstrap 5**
