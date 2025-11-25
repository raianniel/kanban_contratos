# Sistema de Controle de Permissões

## Visão Geral

O sistema implementa controle granular de permissões por fase do Kanban, permitindo que apenas usuários autorizados possam mover contratos para determinados status.

## Grupos de Usuários

### Admin (Administrador)
- **Permissão**: Acesso total a todas as fases
- **Como configurar**: Marcar usuário como "staff" no Django Admin
- **Responsabilidades**:
  - Gerenciar todos os contratos
  - Cancelar e reabrir contratos
  - Configurar permissões de outros usuários

### Gerente
- **Permissão**: Acesso a todas as fases exceto cancelamento
- **Como configurar**: Adicionar usuário ao grupo "gerente"
- **Responsabilidades**:
  - Supervisionar todos os processos
  - Mover contratos entre fases
  - Não pode cancelar contratos (apenas admin)

### Analista
- **Permissão**: Validação de dados
- **Como configurar**: Adicionar usuário ao grupo "analista"
- **Fases permitidas**:
  - Validação de dados

### Analista de Crédito
- **Permissão**: Análise de crédito
- **Como configurar**: Adicionar usuário ao grupo "analista_credito"
- **Fases permitidas**:
  - Análise de crédito

### Jurídico
- **Permissão**: Elaboração e aprovação de contratos
- **Como configurar**: Adicionar usuário ao grupo "juridico"
- **Fases permitidas**:
  - Elaboração do contrato
  - Minuta em aprovação

### Vistoriador
- **Permissão**: Requisição de vistoria
- **Como configurar**: Adicionar usuário ao grupo "vistoriador"
- **Fases permitidas**:
  - Requisição de vistoria

### Financeiro
- **Permissão**: Lançamentos financeiros
- **Como configurar**: Adicionar usuário ao grupo "financeiro"
- **Fases permitidas**:
  - Requisição de lançamento financeiro

## Mapeamento de Permissões

| Fase | Admin | Gerente | Analista | Analista Crédito | Jurídico | Vistoriador | Financeiro |
|------|-------|---------|----------|------------------|----------|-------------|------------|
| Validação de dados | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Análise de crédito | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ |
| Elaboração do contrato | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Requisição de vistoria | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ |
| Minuta em aprovação | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| Assinatura eletrônica | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Requisição de lançamento | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Contrato assinado | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Contrato cancelado | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |

## Configuração Inicial

### 1. Criar Grupos

Execute o script de configuração:

```bash
python configurar_permissoes.py
```

### 2. Adicionar Usuários aos Grupos

Via Django Admin:

1. Acesse http://localhost:8000/admin/auth/user/
2. Clique no usuário desejado
3. Na seção "Permissões", role até "Grupos"
4. Selecione os grupos apropriados
5. Clique em "Salvar"

Via Python Shell:

```python
from django.contrib.auth.models import User, Group

# Obter usuário
usuario = User.objects.get(username='joao.silva')

# Adicionar ao grupo
grupo = Group.objects.get(name='analista_credito')
usuario.groups.add(grupo)
```

## Comportamento no Sistema

### No Kanban

- Usuários só podem arrastar cards para colunas que têm permissão
- Ao tentar mover para coluna sem permissão, aparece mensagem de erro
- Cards ficam visualmente iguais, mas drag & drop é bloqueado

### Mensagens de Erro

Quando usuário tenta mover sem permissão:

```
❌ Você não tem permissão para mover contratos para "Análise de crédito"
```

### Regras Especiais

1. **Contrato Cancelado**: Apenas admin pode cancelar ou reabrir
2. **Responsável**: Sempre pode editar o contrato, mas não mover sem permissão
3. **Superusuário**: Ignora todas as restrições

## Exemplo de Fluxo

### Cenário: Processo Completo

1. **Analista** cria contrato → Validação de dados
2. **Analista** valida dados → move para Análise de crédito
3. **Analista de Crédito** analisa → move para Elaboração do contrato
4. **Jurídico** elabora contrato → move para Requisição de vistoria
5. **Vistoriador** requisita vistoria → move para Minuta em aprovação
6. **Jurídico** aprova minuta → move para Assinatura eletrônica
7. **Gerente** obtém assinatura → move para Requisição de lançamento
8. **Financeiro** lança no sistema → move para Contrato assinado
9. **Admin** (se necessário) cancela → move para Contrato cancelado

## Dicas de Uso

### Para Administradores

- Crie usuários com perfis específicos
- Não dê permissão de "gerente" para todos
- Monitore quem tem acesso a cancelamento

### Para Gerentes

- Você pode mover contratos em qualquer fase
- Use isso para desbloquear processos travados
- Não pode cancelar - solicite ao admin

### Para Usuários Específicos

- Foque apenas na sua área de atuação
- Se precisar mover para outra fase, solicite ao gerente
- Sempre pode editar contratos que você criou

## Solução de Problemas

### Usuário não consegue mover card

1. Verificar se está no grupo correto
2. Verificar se o grupo tem permissão para aquela fase
3. Verificar se não é contrato cancelado (só admin reabre)

### Como dar acesso temporário

```python
# Adicionar ao grupo gerente temporariamente
usuario.groups.add(Group.objects.get(name='gerente'))

# Remover depois
usuario.groups.remove(Group.objects.get(name='gerente'))
```

### Como ver permissões de um usuário

```python
from contratos.permissions import obter_status_permitidos_usuario

status_permitidos = obter_status_permitidos_usuario(usuario)
print(status_permitidos)
```

## Personalização

Para alterar as permissões, edite o arquivo `contratos/permissions.py`:

```python
PERMISSOES_STATUS = {
    'VALIDACAO_DADOS': ['admin', 'gerente', 'analista'],
    # Adicione ou remova grupos conforme necessário
}
```

Após alterar, reinicie o servidor Django.
