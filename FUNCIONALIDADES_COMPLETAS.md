# T2 Web - Funcionalidades Completas

## 📋 Índice

1. [Visualização Kanban](#visualização-kanban)
2. [Gestão de Contratos](#gestão-de-contratos)
3. [Sistema de Anexos](#sistema-de-anexos)
4. [Anexos Obrigatórios](#anexos-obrigatórios)
5. [Sistema de Permissões](#sistema-de-permissões)
6. [Filtros e Busca](#filtros-e-busca)
7. [Dashboard](#dashboard)
8. [Interface](#interface)

---

## 1. Visualização Kanban

### 9 Colunas de Status (Ordem Fixa)

1. **Validação de dados** (cinza)
2. **Análise de crédito** (laranja)
3. **Elaboração do contrato** (mostarda)
4. **Requisição de vistoria** (teal)
5. **Minuta em aprovação** (verde)
6. **Assinatura eletrônica** (dourado)
7. **Requisição de lançamento** (roxo)
8. **Contrato assinado** (azul)
9. **Contrato cancelado** (vermelho - terminal)

### Recursos

- ✅ **Drag & Drop**: Arraste cards entre colunas
- ✅ **Reversão Automática**: Card volta se cancelar modal
- ✅ **Contadores**: Número de cards por coluna
- ✅ **Scroll Horizontal**: Layout responsivo
- ✅ **Cores Personalizadas**: Fácil identificação visual
- ✅ **Animações**: Transições suaves

### Validações

- ✅ Apenas admin pode reabrir contratos cancelados
- ✅ Validação de permissões por grupo
- ✅ Confirmação obrigatória para anexos faltantes

---

## 2. Gestão de Contratos

### Criar Contrato

**Acesso**: Kanban → Botão "Novo"

**Campos**:
- Nome da negociação
- Status inicial
- **Locatário**:
  - Nome
  - Tipo (PF/PJ)
  - CPF/CNPJ
- **Imóvel**:
  - Endereço
  - Código
- **Vigência**:
  - Data início
  - Data fim
  - Valor do aluguel
- **Garantia**:
  - Tipo (Caução, Fiador, Seguro, Título)
- **Responsável**: Usuário logado (automático)
- **Anexos**: Múltiplos arquivos com dropdown

**Validações**:
- Data fim > Data início
- Valor > 0
- CPF/CNPJ válido
- Tipo de arquivo permitido

### Editar Contrato

**Acesso**: 
- Kanban → Botão "Editar" no card
- Detalhes → Botão "Editar"
- Admin → Redireciona para formulário simples

**Permissões**:
- Responsável pode editar
- Admin pode editar qualquer contrato
- Apenas admin pode alterar responsável

**Recursos**:
- Todos os campos editáveis
- Gerenciar anexos (adicionar/remover)
- Histórico automático de mudanças

### Visualizar Detalhes

**Acesso**: Kanban → Botão "Ver" no card

**Informações**:
- Todos os dados do contrato
- Lista de anexos com visualizador
- Histórico de mudanças de status
- Badges de status e vencimento
- Botão "Baixar Todos os Anexos" (ZIP)

### Cancelar Contrato

**Acesso**: Mover para "Contrato Cancelado"

**Comportamento**:
- Modal solicita motivo (obrigatório)
- Registra no histórico
- Apenas admin pode reabrir

---

## 3. Sistema de Anexos

### Upload de Arquivos

**Múltiplos Arquivos**:
- Botão "+ Adicionar Mais Arquivos"
- Sem limite de quantidade
- Upload simultâneo

**Tipos Permitidos**:
- PDF (.pdf)
- Imagens (.jpg, .jpeg, .png)
- Word (.doc, .docx)

**Campos por Anexo**:
- **Tipo de Documento**: Dropdown com lista
- **Arquivo**: Upload
- **Observação**: Texto opcional

### Visualizar Anexos

**Visualizador Inline**:
- PDF: Iframe com visualização completa
- Imagens: Exibição direta
- Modal grande para melhor visualização

**Download**:
- Individual: Link em cada anexo
- Todos: Botão "Baixar Todos" (ZIP)

### Gerenciar Anexos

**Adicionar**:
- Formulário de edição
- Seção "Adicionar Novos Anexos"
- Múltiplos de uma vez

**Remover**:
- Checkbox em cada anexo
- Pode marcar vários
- Confirmação ao salvar

**Informações**:
- Descrição do documento
- Data e hora de envio
- Usuário que enviou
- Tamanho do arquivo

### Detecção Automática

Sistema marca automaticamente:

**Laudo de Vistoria**:
- "Laudo de Vistoria" (exato)
- "laudo" (case-insensitive)

**Contrato Assinado**:
- "Contrato Assinado" (exato)
- "assinado" (case-insensitive)

**Processos Judiciais**:
- "Processos Judiciais" (exato)
- "processos" (case-insensitive)

**Protestos**:
- "Protestos" (exato)
- "protesto" (case-insensitive)

**Restrições de Crédito**:
- "Restrições de Crédito" (exato)
- "SPC", "SERASA" (exato)
- "restrições", "restricoes" (case-insensitive)

---

## 4. Anexos Obrigatórios

### Análise de Crédito (3 documentos)

**Obrigatórios**:
1. Verificação de Processos Judiciais
2. Busca Geral de Protestos
3. Consulta de Restrições de Crédito (SPC/SERASA)

**Comportamento**:
- Pode ENTRAR livremente
- Ao SAIR sem anexos:
  - Modal lista faltantes
  - Digite "CONFIRMAR" para prosseguir
  - Card volta se cancelar

### Requisição de Vistoria (1 documento)

**Obrigatório**:
- Laudo de Vistoria

**Comportamento**: Igual Análise de Crédito

### Assinatura Eletrônica (1 documento)

**Obrigatório**:
- Contrato Assinado

**Comportamento**: Igual Análise de Crédito

### Modal de Confirmação

**Elementos**:
- Cabeçalho amarelo com ⚠️
- Mensagem clara do que falta
- Campo para digitar "CONFIRMAR"
- Botões "Voltar" e "Confirmar"

**Validação**:
- Case-sensitive (CONFIRMAR ≠ confirmar)
- Palavra exata
- Reversão automática se cancelar

---

## 5. Sistema de Permissões

### 7 Grupos de Usuários

**1. Administrador**:
- Acesso total
- Todas as fases
- Reabrir contratos cancelados
- Gerenciar usuários

**2. Gerente**:
- Todas as fases
- Visualizar tudo
- Não pode reabrir cancelados

**3. Analista**:
- Validação de dados
- Elaboração do contrato
- Minuta em aprovação

**4. Analista de Crédito**:
- Análise de crédito
- Visualizar dados

**5. Jurídico**:
- Elaboração do contrato
- Minuta em aprovação

**6. Vistoriador**:
- Requisição de vistoria

**7. Financeiro**:
- Requisição de lançamento financeiro
- Contratos assinados

### Controle Granular

**Por Fase**:
- Cada grupo tem fases permitidas
- Validação no backend
- Mensagem clara se negado

**Por Ação**:
- Criar: Todos os usuários
- Editar: Responsável ou admin
- Cancelar: Admin ou responsável
- Reabrir: Apenas admin

### Configuração

```bash
python configurar_permissoes.py
```

**Adicionar Usuário a Grupo**:
1. Django Admin → Usuários
2. Selecionar usuário
3. Seção "Grupos"
4. Adicionar ao grupo desejado

---

## 6. Filtros e Busca

### Filtro de Texto

**Busca em**:
- Nome da negociação
- Nome do locatário
- Endereço do imóvel

**Comportamento**:
- Busca parcial (case-insensitive)
- Atualização em tempo real
- Destaque nos resultados

### Filtro por Responsável

**Dropdown**:
- Lista todos os usuários ativos
- Opção "Todos"
- Filtra cards instantaneamente

### Filtro por Tipo de Locatário

**Opções**:
- Todos
- Pessoa Física (PF)
- Pessoa Jurídica (PJ)

**Comportamento**:
- Radio buttons
- Filtra instantaneamente

### Badges nos Cards

**Tipo de Garantia**:
- Caução (azul)
- Fiador (verde)
- Seguro (laranja)
- Título (roxo)

**Vencimento**:
- Verde: > 30 dias
- Amarelo: ≤ 30 dias
- Vermelho: Vencido

**SLA**:
- Mostra "+Xd" se excedido
- Vermelho

**Anexos**:
- Ícone de clipe se tem anexos

---

## 7. Dashboard

### Estatísticas

**Contadores**:
- Total de contratos
- Por status
- Vencendo em 30 dias
- Vencidos
- Por responsável

**Gráficos**:
- Distribuição por status
- Contratos por mês
- Taxa de conversão

### Tabelas

**Contratos Atrasados**:
- Nome
- Status
- Dias de atraso
- Responsável
- Link para detalhes

**Próximos Vencimentos**:
- Nome
- Data de vencimento
- Dias restantes
- Link para ação

### Acesso

**URL**: http://localhost:8000/dashboard  
**Navbar**: Botão "Dashboard"

---

## 8. Interface

### Tema

**Cores**:
- Navbar: Preto (#000000)
- Background: Branco (#ffffff)
- Cards: Brancos com borda cinza
- Texto: Preto
- Hover: Cinza claro

**Logo**:
- T2 Web Real Estate
- Branca (para navbar preta)
- 40px de altura
- Clicável (vai para Kanban)

### Responsividade

**Desktop**:
- Colunas lado a lado
- Scroll horizontal
- Largura fixa por coluna

**Tablet**:
- Colunas menores
- Scroll horizontal
- Touch-friendly

**Mobile**:
- Colunas estreitas
- Scroll horizontal
- Botões maiores

### Acessibilidade

**Recursos**:
- Contraste adequado
- Ícones descritivos
- Tooltips informativos
- Mensagens claras
- Feedback visual

### Animações

**Drag & Drop**:
- Fantasma semi-transparente
- Rotação leve ao arrastar
- Transição suave ao soltar

**Hover**:
- Sombra sutil
- Elevação do card
- Mudança de cor

**Modais**:
- Fade in/out
- Backdrop escurecido
- Animação suave

---

## 🎯 Resumo de Funcionalidades

| Funcionalidade | Status | Detalhes |
|----------------|--------|----------|
| Kanban 9 colunas | ✅ | Drag & drop com reversão |
| Criar contrato | ✅ | Formulário completo |
| Editar contrato | ✅ | Formulário + anexos |
| Anexos múltiplos | ✅ | Upload, visualizar, remover |
| Anexos obrigatórios | ✅ | 3 fases com confirmação |
| Permissões | ✅ | 7 grupos de usuários |
| Filtros | ✅ | Texto, responsável, tipo |
| Dashboard | ✅ | Estatísticas e gráficos |
| Histórico | ✅ | Auditoria completa |
| Tema preto/branco | ✅ | Logo T2 Web |

---

## 📚 Documentação Relacionada

- [README.md](README.md) - Visão geral
- [COMO_USAR.md](COMO_USAR.md) - Guia de uso
- [PERMISSOES.md](PERMISSOES.md) - Detalhes de permissões
- [ANALISE_CREDITO.md](ANALISE_CREDITO.md) - Anexos obrigatórios
- [VSCODE_SETUP.md](VSCODE_SETUP.md) - Configuração VS Code

---

**Versão**: 2.0  
**Atualizado**: Outubro 2025
