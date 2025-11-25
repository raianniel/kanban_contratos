# Como Usar o Sistema - Guia Prático

## 📝 Como Adicionar Novos Contratos

Existem **duas formas** de adicionar contratos no sistema:

---

## Opção 1: Via Django Admin (Recomendado) ⭐

Esta é a forma mais completa e fácil de adicionar contratos.

### Passo a Passo

#### 1. Acessar o Admin

Abra o navegador e acesse: http://localhost:8000/admin

Faça login com suas credenciais (admin / admin123)

#### 2. Navegar até Contratos

No painel do Django Admin:
1. Procure a seção **"CONTRATOS"**
2. Clique em **"Contratos"**
3. Você verá a lista de todos os contratos

#### 3. Adicionar Novo Contrato

1. Clique no botão **"ADICIONAR CONTRATO"** (canto superior direito)
2. Preencha o formulário com os dados do contrato

### Campos do Formulário

**Identificação**
- **Nome da negociação**: Nome descritivo do contrato (ex: "Contrato Apt 101 - João Silva")
- **Status**: Escolha o status inicial (padrão: Validação de dados)

**Dados do Locatário**
- **Nome do locatário**: Nome completo
- **Tipo de locatário**: Pessoa Física (PF) ou Pessoa Jurídica (PJ)
- **Documento**: CPF (para PF) ou CNPJ (para PJ)

**Dados do Imóvel**
- **Endereço do imóvel**: Endereço completo
- **Código do imóvel**: Código interno de identificação

**Vigência e Valores**
- **Início da vigência**: Data de início do contrato
- **Fim da vigência**: Data de término do contrato
- **Valor do aluguel**: Valor mensal (ex: 1500.00)

**Garantia**
- **Tipo de garantia**: Escolha entre:
  - Caução
  - Fiador
  - Seguro Fiança
  - Título de Capitalização
  - Nenhuma

**Controle**
- **Responsável**: Usuário responsável pelo contrato
- **Prazo da fase (dias)**: SLA da fase atual (padrão: 5 dias)
- **Possui anexos**: Marque se há documentos anexados

**Cancelamento** (apenas se status for "Contrato cancelado")
- **Motivo do cancelamento**: Obrigatório ao cancelar

#### 4. Salvar

Clique em **"SALVAR"** no final da página.

O contrato aparecerá automaticamente no Kanban! 🎉

---

## Opção 2: Via Python Shell (Avançado)

Para usuários que preferem programar ou precisam adicionar muitos contratos de uma vez.

### Passo a Passo

#### 1. Abrir Django Shell

No terminal (com ambiente virtual ativado):

```bash
python manage.py shell
```

#### 2. Importar Modelos

```python
from contratos.models import Contrato
from django.contrib.auth.models import User
from datetime import date, timedelta
```

#### 3. Criar Contrato

```python
# Buscar um usuário responsável
responsavel = User.objects.first()

# Criar o contrato
contrato = Contrato.objects.create(
    nome_negociacao="Contrato Apt 202 - Maria Santos",
    status="VALIDACAO_DADOS",
    locatario_nome="Maria Santos",
    locatario_tipo="PF",
    locatario_documento="123.456.789-00",
    imovel_endereco="Rua das Flores, 202, Centro",
    imovel_codigo="APT-202",
    inicio_vigencia=date.today(),
    fim_vigencia=date.today() + timedelta(days=365),
    valor_aluguel=1500.00,
    tipo_garantia="CAUCAO",
    responsavel=responsavel,
    prazo_fase_dias=5,
    possui_anexos=False
)

print(f"Contrato criado: {contrato.nome_negociacao}")
```

#### 4. Sair do Shell

```python
exit()
```

---

## 📊 Como Visualizar Contratos

### No Kanban

Acesse: http://localhost:8000/kanban

Você verá todos os contratos organizados por status em colunas.

### No Dashboard

Acesse: http://localhost:8000/kanban/dashboard

Veja estatísticas, contratos atrasados e distribuição por status.

### No Admin

Acesse: http://localhost:8000/admin

Lista completa com filtros e busca avançada.

---

## 🔄 Como Mover Contratos Entre Status

### Via Kanban (Drag & Drop)

1. Acesse o Kanban: http://localhost:8000/kanban
2. **Clique e segure** o card do contrato
3. **Arraste** para a coluna desejada
4. **Solte** o card na nova coluna
5. O status será atualizado automaticamente

**Atenção:** Ao mover para "Contrato cancelado", será solicitado o motivo.

### Via Admin

1. Acesse: http://localhost:8000/admin
2. Clique no contrato que deseja editar
3. Altere o campo **"Status"**
4. Clique em **"SALVAR"**

---

## 🔍 Como Filtrar Contratos

No Kanban, use os filtros no topo da página:

### Busca por Texto
Digite qualquer texto para buscar em:
- Nome da negociação
- Nome do locatário
- Endereço do imóvel

### Filtro por Responsável
Selecione um usuário específico no dropdown.

### Filtro por Tipo de Locatário
- **Todos**: Mostra PF e PJ
- **PF**: Apenas Pessoa Física
- **PJ**: Apenas Pessoa Jurídica

Clique em **"Filtrar"** para aplicar.

---

## 👁️ Como Ver Detalhes de um Contrato

### Via Kanban

1. Encontre o card do contrato
2. Clique em **"Ver detalhes"**
3. Você verá:
   - Todas as informações do contrato
   - Histórico de mudanças de status
   - Lista de anexos
   - Badges coloridos

### Via Admin

1. Acesse: http://localhost:8000/admin
2. Clique no nome do contrato na lista
3. Visualize/edite todos os campos

---

## 📎 Como Adicionar Anexos

### Via Admin

1. Acesse o contrato no Admin
2. Role até a seção **"ANEXOS DO CONTRATO"**
3. Clique em **"Adicionar outro Anexo do contrato"**
4. Preencha:
   - **Arquivo**: Clique em "Escolher arquivo" e selecione
   - **Descrição**: Descreva o documento (ex: "CPF do locatário")
5. Clique em **"SALVAR"**

O ícone de anexo aparecerá no card do Kanban! 📎

---

## ✏️ Como Editar um Contrato

### Via Admin (Recomendado)

1. Acesse: http://localhost:8000/admin
2. Encontre o contrato na lista
3. Clique no nome do contrato
4. Edite os campos desejados
5. Clique em **"SALVAR"**

### Campos que Podem Ser Editados

Todos os campos podem ser editados, exceto:
- Data de criação (criado_em)
- Data de atualização (atualizado_em) - atualiza automaticamente

---

## 🗑️ Como Cancelar um Contrato

### Via Kanban

1. Arraste o card para a coluna **"Contrato cancelado"**
2. Um modal aparecerá solicitando o **motivo**
3. Digite o motivo do cancelamento
4. Clique em **"Confirmar"**

### Via Admin

1. Acesse o contrato no Admin
2. Altere o **Status** para "Contrato cancelado"
3. Preencha o campo **"Motivo do cancelamento"** (obrigatório)
4. Clique em **"SALVAR"**

**Atenção:** Contratos cancelados não podem ser movidos. Apenas administradores podem reabri-los.

---

## 🔓 Como Reabrir um Contrato Cancelado

Apenas **administradores** podem reabrir contratos cancelados.

### Via Admin

1. Acesse o contrato cancelado no Admin
2. Altere o **Status** para outro status (ex: "Validação de dados")
3. Limpe o campo **"Motivo do cancelamento"** (opcional)
4. Clique em **"SALVAR"**

O contrato voltará a aparecer no Kanban na nova coluna.

---

## 👥 Como Gerenciar Usuários

### Criar Novo Usuário

1. Acesse: http://localhost:8000/admin
2. Clique em **"Usuários"** (seção AUTENTICAÇÃO E AUTORIZAÇÃO)
3. Clique em **"ADICIONAR USUÁRIO"**
4. Preencha:
   - **Nome de usuário**: Login do usuário
   - **Senha**: Senha inicial
5. Clique em **"SALVAR"**
6. Preencha dados adicionais:
   - Nome completo
   - Email
   - Permissões
7. Clique em **"SALVAR"** novamente

### Tornar Usuário Administrador

1. Acesse o usuário no Admin
2. Marque as opções:
   - ☑️ **Status de equipe** (permite acessar admin)
   - ☑️ **Status de superusuário** (acesso total)
3. Clique em **"SALVAR"**

---

## 📈 Como Interpretar o Dashboard

Acesse: http://localhost:8000/kanban/dashboard

### Métricas Principais

**Total de Contratos**
- Número total de contratos no sistema (exceto cancelados)

**Contratos com SLA Excedido**
- Contratos que estão na fase atual há mais tempo que o prazo definido

**Taxa de Sucesso**
- Percentual de contratos dentro do prazo

### Tabelas

**Distribuição por Status**
- Quantidade e percentual de contratos em cada status

**Top 10 Responsáveis**
- Usuários com mais contratos atribuídos

**Contratos Atrasados**
- Lista detalhada dos contratos com SLA excedido
- Mostra quantos dias de atraso

---

## 🎨 Entendendo os Badges

### Badge de Garantia
- **Azul**: Caução
- **Verde**: Fiador
- **Laranja**: Seguro Fiança
- **Roxo**: Título de Capitalização
- **Cinza**: Nenhuma

### Badge de Vencimento
- **Verde**: Mais de 30 dias para vencer
- **Amarelo**: 30 dias ou menos para vencer
- **Vermelho**: Contrato vencido

### Badge de SLA
- **Vermelho "+Xd"**: Contrato está X dias atrasado na fase atual

### Ícone de Anexo
- **📎**: Contrato possui documentos anexados

---

## 🔧 Comandos Úteis

### Popular com Dados de Exemplo

```bash
python popular_dados.py
```

Cria 33 contratos de exemplo para testar.

### Ver Todos os Contratos no Shell

```bash
python manage.py shell
```

```python
from contratos.models import Contrato
contratos = Contrato.objects.all()
for c in contratos:
    print(f"{c.nome_negociacao} - {c.get_status_display()}")
```

### Contar Contratos por Status

```python
from contratos.models import Contrato
from django.db.models import Count

stats = Contrato.objects.values('status').annotate(total=Count('id'))
for s in stats:
    print(f"{s['status']}: {s['total']}")
```

### Listar Contratos Atrasados

```python
from contratos.models import Contrato

atrasados = [c for c in Contrato.objects.all() if c.sla_excedido]
for c in atrasados:
    print(f"{c.nome_negociacao} - {c.dias_na_fase_atual} dias na fase")
```

---

## 💡 Dicas e Boas Práticas

### Organização

1. **Nomeie contratos de forma clara**: Use padrão como "Contrato [Imóvel] - [Locatário]"
2. **Atribua responsáveis**: Sempre defina um responsável para cada contrato
3. **Configure SLA realista**: Ajuste o prazo de cada fase conforme seu processo
4. **Anexe documentos**: Mantenha toda documentação anexada ao contrato

### Workflow

1. **Comece em "Validação de dados"**: Novos contratos sempre iniciam aqui
2. **Mova progressivamente**: Avance pelas colunas conforme o processo
3. **Use o Dashboard**: Monitore contratos atrasados diariamente
4. **Registre motivos**: Ao cancelar, sempre documente o motivo

### Performance

1. **Use filtros**: Em vez de rolar, filtre por responsável ou tipo
2. **Arquive cancelados**: Contratos cancelados não aparecem no Kanban por padrão
3. **Limpe dados antigos**: Periodicamente, revise contratos muito antigos

### Backup

1. **Copie db.sqlite3**: Faça backup regular do arquivo de banco
2. **Exporte para JSON**: Use `dumpdata` para backup portátil
3. **Guarde anexos**: A pasta `media/` contém todos os uploads

---

## 🆘 Problemas Comuns

### Contrato não aparece no Kanban

**Causa**: Filtros ativos ou status cancelado

**Solução**: 
- Limpe os filtros (recarregue a página)
- Verifique se o status não é "Contrato cancelado"

### Não consigo mover o card

**Causa**: Contrato cancelado ou sem permissão

**Solução**:
- Contratos cancelados não podem ser movidos
- Verifique se está logado

### Badge de SLA não aparece

**Causa**: Contrato ainda dentro do prazo

**Solução**:
- Badge só aparece quando SLA é excedido
- Verifique o campo `prazo_fase_dias`

### Erro ao cancelar sem motivo

**Causa**: Motivo é obrigatório

**Solução**:
- Sempre preencha o motivo ao cancelar
- O modal solicitará automaticamente

---

## 📚 Recursos Adicionais

### Documentação

- **README.md** - Visão geral do sistema
- **INICIO_RAPIDO.md** - Instalação rápida
- **FUNCIONALIDADES.md** - Lista completa de recursos

### Atalhos do Django Admin

- **Ctrl+S**: Salvar (em alguns navegadores)
- **Tab**: Navegar entre campos
- **Shift+Tab**: Voltar campo

### URLs Úteis

- **Home**: http://localhost:8000
- **Kanban**: http://localhost:8000/kanban
- **Dashboard**: http://localhost:8000/kanban/dashboard
- **Admin**: http://localhost:8000/admin
- **Logout**: http://localhost:8000/admin/logout

---

## ✅ Resumo Rápido

**Para adicionar contrato:**
1. Acesse http://localhost:8000/admin
2. Clique em "Contratos" → "Adicionar contrato"
3. Preencha o formulário
4. Salve

**Para mover contrato:**
1. Acesse http://localhost:8000/kanban
2. Arraste o card para outra coluna
3. Confirme (se necessário)

**Para ver detalhes:**
1. Clique em "Ver detalhes" no card
2. Ou acesse via Admin

**Para filtrar:**
1. Use os campos no topo do Kanban
2. Clique em "Filtrar"

---

**Pronto para usar!** 🚀

Se tiver dúvidas, consulte a documentação completa ou os comentários no código.
