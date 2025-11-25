# Funcionalidades - Sistema Kanban T2 v3.0

**Versão:** 3.0.0 com Cadastro Público  
**Data:** 08 de outubro de 2025

---

## 🚀 Novidades da Versão 3.0

### 1. Cadastro Público de Contratos

- **URL:** `/cadastro/`
- **Descrição:** Um formulário público e responsivo permite que clientes iniciem o processo de locação sem necessidade de login.
- **Fluxo:**
  1. Cliente preenche dados pessoais, do imóvel e do contrato.
  2. Ao enviar, um novo contrato é criado no sistema.
  3. O contrato entra automaticamente no status **"Validação de Dados"**.
  4. Uma página de sucesso é exibida com um resumo das informações.
- **Segurança:** Protegido com CSRF token.

### 2. Campos de Email e Telefone Corrigidos

- **Problema:** Email e telefone eram campos de anexo.
- **Solução:** Agora são campos de texto (`EmailField` e `CharField`) no formulário e no banco de dados, facilitando a entrada de dados.

### 3. Página de Sucesso Pós-Cadastro

- **URL:** `/cadastro/sucesso/<id>/`
- **Descrição:** Após o envio do formulário público, o cliente é redirecionado para uma página de confirmação que exibe:
  - Mensagem de sucesso.
  - Resumo dos dados cadastrados.
  - Próximos passos e informações de contato.

---

## ✅ Funcionalidades Principais

### 1. Kanban Board Interativo

- **Descrição:** Visualização de todos os contratos em um quadro Kanban com colunas representando cada fase do processo.
- **Recursos:**
  - **Drag & Drop:** Mova cards entre colunas para atualizar o status.
  - **Filtros:** Filtre contratos por texto, responsável ou tipo de locatário.
  - **Badges Visuais:** Identifique rapidamente o prazo e o responsável.
  - **Ações Rápidas:** Acesse "Ver" e "Editar" diretamente do card.

### 2. Dashboard de Métricas

- **Descrição:** Um painel com as principais métricas e estatísticas do processo de locação.
- **Indicadores:**
  - Total de Contratos
  - Contratos Atrasados (SLA excedido)
  - Taxa de Sucesso
  - Contratos por Status (tabela)
  - Top 10 Responsáveis (tabela)
  - Contratos com SLA Excedido (lista)

### 3. Gestão de Contratos Completa

- **Criação:** Formulário interno para criação de contratos por usuários logados.
- **Edição:** Formulário completo para editar todos os dados de um contrato.
- **Detalhes:** Visão 360º do contrato com todas as informações, histórico e anexos.

### 4. Sistema de Anexos

- **Upload Múltiplo:** Adicione vários documentos de uma vez.
- **Visualização Inline:** Visualize PDFs e imagens diretamente no navegador sem precisar baixar.
- **Download:** Baixe anexos individualmente ou todos de uma vez em um arquivo ZIP.
- **Controle de Versão:** Histórico de quem enviou e quando.

### 5. Histórico de Status

- **Descrição:** Rastreamento completo de todas as mudanças de status de um contrato.
- **Informações:**
  - Status anterior e novo.
  - Data e hora da alteração.
  - Usuário que realizou a mudança.
  - Observações.

### 6. Sistema de Permissões

- **Admin vs. Usuário:**
  - **Admin:** Acesso total, pode ver e editar todos os contratos.
  - **Usuário:** Acesso restrito, pode ver e editar apenas os contratos pelos quais é responsável.
- **Segurança:** Rotas protegidas com `@login_required`.

---

## 🎨 Tema T2 Real Estate

- **Identidade Visual:** Todo o sistema (interno e público) utiliza a paleta de cores oficial da T2.
- **Componentes Estilizados:**
  - Navbar, botões, cards, tabelas, formulários e badges.
- **Responsividade:** Layout adaptado para desktops, tablets e celulares.
- **CSS Customizado:** Estilos centralizados em `/static/css/t2_theme.css` para fácil manutenção.

---

## ⚙️ Configurações e Melhorias

- **Banco de Dados:** Suporte a SQLite (desenvolvimento) e MySQL (produção).
- **Variáveis de Ambiente:** Configurações sensíveis (chaves, senhas) gerenciadas via arquivo `.env`.
- **Segurança:**
  - `X_FRAME_OPTIONS = 'SAMEORIGIN'` para permitir visualização de anexos.
  - Proteção contra CSRF em todos os formulários.
- **Performance:** Arquivos estáticos otimizados e servidos via Nginx em produção.

