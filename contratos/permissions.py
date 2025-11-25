from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Contrato


# Mapeamento de permissões por status
PERMISSOES_STATUS = {
    'VALIDACAO_DADOS': ['admin', 'Gerente', 'Analista'],
    'ANALISE_CREDITO': ['admin', 'Gerente', 'Analista de Crédito'],
    'ELABORACAO_CONTRATO': ['admin', 'Gerente', 'Jurídico'],
    'REQUISICAO_VISTORIA': ['admin', 'Gerente', 'Vistoriador'],
    'MINUTA_APROVACAO': ['admin', 'Gerente', 'Jurídico'],
    'ASSINATURA_ELETRONICA': ['admin', 'Gerente'],
    'REQUISICAO_LANCAMENTO': ['admin', 'Gerente', 'Financeiro'],
    'CONTRATO_ASSINADO': ['admin', 'Gerente'],
    'CONTRATO_CANCELADO': ['admin'],  # Apenas admin
}


def usuario_pode_mover_para_status(user, status_destino):
    """
    Verifica se o usuário tem permissão para mover um contrato para o status especificado
    """
    # Superusuário pode tudo
    if user.is_superuser:
        return True
    
    # Verificar se usuário pertence a algum grupo com permissão
    grupos_permitidos = PERMISSOES_STATUS.get(status_destino, [])
    
    # Se 'admin' está na lista, verificar se é staff
    if 'admin' in grupos_permitidos and user.is_staff:
        return True
    
    # Verificar grupos do usuário
    grupos_usuario = user.groups.values_list('name', flat=True)
    
    for grupo in grupos_usuario:
        if grupo in grupos_permitidos:
            return True
    
    return False


def criar_grupos_permissoes():
    """
    Cria os grupos de permissões necessários para o sistema
    """
    grupos = [
        ('Gerente', 'Gerente - Acesso total exceto cancelamento'),
        ('Analista', 'Analista - Validação de dados'),
        ('Analista de Crédito', 'Analista de Crédito - Análise de crédito'),
        ('Jurídico', 'Jurídico - Elaboração e aprovação de contratos'),
        ('Vistoriador', 'Vistoriador - Requisição de vistoria'),
        ('Financeiro', 'Financeiro - Lançamentos financeiros'),
    ]
    
    for nome_grupo, descricao in grupos:
        grupo, created = Group.objects.get_or_create(name=nome_grupo)
        if created:
            print(f"Grupo '{nome_grupo}' criado: {descricao}")
    
    print("Grupos de permissões criados com sucesso!")


def obter_status_permitidos_usuario(user):
    """
    Retorna lista de status que o usuário pode mover contratos
    """
    status_permitidos = []
    
    for status, _ in Contrato.STATUS_CHOICES:
        if usuario_pode_mover_para_status(user, status):
            status_permitidos.append(status)
    
    return status_permitidos
