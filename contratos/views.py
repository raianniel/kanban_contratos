from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from django.views.decorators.http import require_POST
from django.utils import timezone
from collections import OrderedDict
from .models import Contrato, HistoricoStatus
from django.contrib.auth.models import User


@login_required
def kanban_view(request):
    """
    View principal do Kanban - exibe todas as colunas com cards agrupados por status
    """
    # Obter parâmetros de filtro
    filtro_texto = request.GET.get('q', '').strip()
    filtro_responsavel = request.GET.get('responsavel', '')
    filtro_tipo_locatario = request.GET.get('tipo_locatario', '')
    
    # Query base
    contratos = Contrato.objects.select_related('responsavel').all()
    
    # Aplicar filtros
    if filtro_texto:
        contratos = contratos.filter(
            Q(nome_negociacao__icontains=filtro_texto) |
            Q(locatario_nome__icontains=filtro_texto) |
            Q(imovel_endereco__icontains=filtro_texto) |
            Q(imovel_codigo__icontains=filtro_texto)
        )
    
    if filtro_responsavel:
        contratos = contratos.filter(responsavel_id=filtro_responsavel)
    
    if filtro_tipo_locatario:
        contratos = contratos.filter(locatario_tipo=filtro_tipo_locatario)
    
    # Agrupar contratos por status mantendo a ordem das colunas
    colunas = OrderedDict()
    
    # Definir ordem das colunas conforme especificação
    ordem_status = [
        'VALIDACAO_DADOS',
        'ANALISE_CREDITO',
        'ELABORACAO_CONTRATO',
        'REQUISICAO_VISTORIA',
        'MINUTA_APROVACAO',
        'ASSINATURA_ELETRONICA',
        'REQUISICAO_LANCAMENTO',
        'CONTRATO_ASSINADO',
        'CONTRATO_CANCELADO',
    ]
    
    # Inicializar todas as colunas
    for status_code in ordem_status:
        status_display = dict(Contrato.STATUS_CHOICES)[status_code]
        colunas[status_code] = {
            'codigo': status_code,
            'titulo': status_display,
            'contratos': [],
            'contador': 0,
            'cor': Contrato().cor_coluna_status() if status_code == 'VALIDACAO_DADOS' else None
        }
    
    # Preencher colunas com contratos filtrados
    for contrato in contratos:
        if contrato.status in colunas:
            colunas[contrato.status]['contratos'].append(contrato)
            colunas[contrato.status]['contador'] += 1
            # Definir cor da coluna baseada no primeiro contrato
            if colunas[contrato.status]['cor'] is None:
                colunas[contrato.status]['cor'] = contrato.cor_coluna_status()
    
    # Obter lista de responsáveis para o filtro
    responsaveis = User.objects.filter(contratos__isnull=False).distinct().order_by('username')
    
    context = {
        'colunas': colunas,
        'responsaveis': responsaveis,
        'filtro_texto': filtro_texto,
        'filtro_responsavel': filtro_responsavel,
        'filtro_tipo_locatario': filtro_tipo_locatario,
        'total_contratos': contratos.count(),
    }
    
    return render(request, 'contratos/kanban.html', context)


@login_required
@require_POST
def mudar_status(request, contrato_id):
    """
    View para mudar o status de um contrato via AJAX (drag & drop)
    """
    from .permissions import usuario_pode_mover_para_status
    
    contrato = get_object_or_404(Contrato, id=contrato_id)
    novo_status = request.POST.get('status')
    motivo_cancelamento = request.POST.get('motivo_cancelamento', '').strip()
    
    # Validar se o novo status é válido
    status_validos = [choice[0] for choice in Contrato.STATUS_CHOICES]
    if novo_status not in status_validos:
        return JsonResponse({
            'success': False,
            'error': 'Status inválido'
        }, status=400)
    
    # Verificar permissão do usuário para mover para este status
    if not usuario_pode_mover_para_status(request.user, novo_status):
        status_display = dict(Contrato.STATUS_CHOICES).get(novo_status, novo_status)
        return JsonResponse({
            'success': False,
            'error': f'Você não tem permissão para mover contratos para "{status_display}"'
        }, status=403)
    
    # Verificar se está tentando reabrir um contrato cancelado
    if contrato.status == 'CONTRATO_CANCELADO' and not request.user.is_staff:
        return JsonResponse({
            'success': False,
            'error': 'Apenas administradores podem reabrir contratos cancelados'
        }, status=403)
    
    # Validar motivo de cancelamento
    if novo_status == 'CONTRATO_CANCELADO' and not motivo_cancelamento:
        return JsonResponse({
            'success': False,
            'error': 'Motivo do cancelamento é obrigatório',
            'require_reason': True
        }, status=400)
    
    # Validar anexos obrigatórios ao SAIR de determinadas fases
    confirmacao = request.POST.get('confirmacao', '').strip()
    
    # Impedir SAÍDA de Requisição de Vistoria sem Laudo
    if contrato.status == 'REQUISICAO_VISTORIA' and novo_status != 'REQUISICAO_VISTORIA':
        if not contrato.laudo_vistoria_anexado:
            # Se não tem confirmação, pedir
            if confirmacao != 'CONFIRMAR':
                return JsonResponse({
                    'success': False,
                    'error': 'Tem certeza que deseja sair dessa fase sem anexar o Laudo de Vistoria?',
                    'require_confirmation': True,
                    'confirmation_message': 'Para sair desta fase sem anexar o Laudo de Vistoria, digite CONFIRMAR:',
                    'confirmation_word': 'CONFIRMAR'
                }, status=400)
    
    # Impedir SAÍDA de Assinatura Eletrônica sem Contrato Assinado
    if contrato.status == 'ASSINATURA_ELETRONICA' and novo_status != 'ASSINATURA_ELETRONICA':
        if not contrato.contrato_assinado_anexado:
            # Se não tem confirmação, pedir
            if confirmacao != 'CONFIRMAR':
                return JsonResponse({
                    'success': False,
                    'error': 'Tem certeza que deseja sair dessa fase sem anexar o Contrato Assinado?',
                    'require_confirmation': True,
                    'confirmation_message': 'Para sair desta fase sem anexar o Contrato Assinado, digite CONFIRMAR:',
                    'confirmation_word': 'CONFIRMAR'
                }, status=400)
    
    # Impedir SAÍDA de Análise de Crédito sem anexos obrigatórios
    if contrato.status == 'ANALISE_CREDITO' and novo_status != 'ANALISE_CREDITO':
        anexos_faltantes = []
        if not contrato.processos_judiciais_anexado:
            anexos_faltantes.append('Verificação de Processos Judiciais')
        if not contrato.protestos_anexado:
            anexos_faltantes.append('Busca Geral de Protestos')
        if not contrato.restricoes_credito_anexado:
            anexos_faltantes.append('Consulta de Restrições de Crédito (SPC/SERASA)')
        
        if anexos_faltantes:
            # Se não tem confirmação, pedir
            if confirmacao != 'CONFIRMAR':
                anexos_texto = ', '.join(anexos_faltantes)
                return JsonResponse({
                    'success': False,
                    'error': f'Tem certeza que deseja sair dessa fase sem anexar: {anexos_texto}?',
                    'require_confirmation': True,
                    'confirmation_message': f'Para sair desta fase sem anexar os documentos de Análise de Crédito, digite CONFIRMAR:',
                    'confirmation_word': 'CONFIRMAR'
                }, status=400)
    
    # Salvar status anterior para histórico
    status_anterior = contrato.status
    
    # Atualizar contrato
    contrato.status = novo_status
    contrato.data_entrada_fase = timezone.now()
    
    if novo_status == 'CONTRATO_CANCELADO':
        contrato.motivo_cancelamento = motivo_cancelamento
    
    contrato.save()
    
    # Criar registro no histórico
    HistoricoStatus.objects.create(
        contrato=contrato,
        status_anterior=status_anterior,
        status_novo=novo_status,
        alterado_por=request.user,
        observacao=motivo_cancelamento if novo_status == 'CONTRATO_CANCELADO' else ''
    )
    
    return JsonResponse({
        'success': True,
        'message': f'Status alterado para {contrato.get_status_display()}',
        'novo_status': novo_status,
        'status_display': contrato.get_status_display()
    })


@login_required
def contrato_detalhe(request, contrato_id):
    """
    View para exibir detalhes de um contrato
    """
    contrato = get_object_or_404(Contrato.objects.select_related('responsavel'), id=contrato_id)
    historico = contrato.historico.select_related('alterado_por').all()[:20]
    anexos = contrato.anexos.select_related('enviado_por').all()
    
    context = {
        'contrato': contrato,
        'historico': historico,
        'anexos': anexos,
    }
    
    return render(request, 'contratos/detalhe.html', context)


@login_required
def dashboard(request):
    """
    View para dashboard com estatísticas gerais
    """
    # Contar contratos por status
    stats_status = Contrato.objects.values('status').annotate(
        total=Count('id')
    ).order_by('status')
    
    # Contratos por responsável
    stats_responsavel = Contrato.objects.values(
        'responsavel__username'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:10]
    
    # Contratos com SLA excedido
    contratos_atrasados = []
    for contrato in Contrato.objects.exclude(status='CONTRATO_CANCELADO'):
        sla_excedido = contrato.sla_excedido()
        if sla_excedido:
            contratos_atrasados.append({
                'contrato': contrato,
                'dias_excedidos': sla_excedido
            })
    
    # Ordenar por dias excedidos
    contratos_atrasados.sort(key=lambda x: x['dias_excedidos'], reverse=True)
    
    context = {
        'stats_status': stats_status,
        'stats_responsavel': stats_responsavel,
        'contratos_atrasados': contratos_atrasados[:20],
        'total_contratos': Contrato.objects.count(),
        'total_atrasados': len(contratos_atrasados),
    }
    
    return render(request, 'contratos/dashboard.html', context)


@login_required
def contrato_criar(request):
    """
    View para criar novo contrato (formulário simplificado para usuários comuns)
    """
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            contrato = Contrato(
                nome_negociacao=request.POST.get('nome_negociacao'),
                status=request.POST.get('status', 'VALIDACAO_DADOS'),
                locatario_nome=request.POST.get('locatario_nome'),
                locatario_tipo=request.POST.get('locatario_tipo'),
                locatario_documento=request.POST.get('locatario_documento'),
                locatario_email=request.POST.get('locatario_email', ''),
                locatario_telefone=request.POST.get('locatario_telefone', ''),
                imovel_endereco=request.POST.get('imovel_endereco'),
                imovel_codigo=request.POST.get('imovel_codigo', ''),
                inicio_vigencia=request.POST.get('inicio_vigencia'),
                fim_vigencia=request.POST.get('fim_vigencia'),
                valor_aluguel=request.POST.get('valor_aluguel'),
                tipo_garantia=request.POST.get('tipo_garantia', 'NENHUMA'),
                observacoes_gerais=request.POST.get('observacoes_gerais', ''),
                responsavel=request.user,  # Usuário logado como responsável
                prazo_fase_dias=request.POST.get('prazo_fase_dias', 5),
            )
            contrato.save()
            
            # Processar anexos (múltiplos arquivos)
            arquivos = request.FILES.getlist('anexos')
            descricoes = request.POST.getlist('descricoes_anexos')
            
            for i, arquivo in enumerate(arquivos):
                descricao = descricoes[i] if i < len(descricoes) else arquivo.name
                from .models import AnexoContrato
                AnexoContrato.objects.create(
                    contrato=contrato,
                    arquivo=arquivo,
                    descricao=descricao,
                    enviado_por=request.user
                )
            
            # Criar registro no histórico
            HistoricoStatus.objects.create(
                contrato=contrato,
                status_anterior='',
                status_novo=contrato.status,
                alterado_por=request.user,
                observacao='Contrato criado'
            )
            
            messages.success(request, f'Contrato "{contrato.nome_negociacao}" criado com sucesso!')
            return redirect('kanban')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar contrato: {str(e)}')
    
    # GET - exibir formulário
    responsaveis = User.objects.filter(is_active=True).order_by('username')
    
    # Documentos necessários por tipo de locatário
    documentos_pf = [
        'Cópia dos Documentos Pessoas: RG/CPF e/ou CNH',
        'Comprovante de Residência',
        'Certidão de Casamento e/ou Atestado de Óbito do Cônjuge',
        'Última Declaração do Imposto de Renda',
        'Verificação de Processos Judiciais',
        'Busca Geral de Protestos',
        'Consulta de Restrições de Crédito (SPC/SERASA)',
        'Laudo de Vistoria',
        'Contrato Assinado'
    ]
    
    documentos_pj = [
        'Contrato Social',
        'Cartão CNPJ',
        'Inscrição Estadual e Municipal',
        'Comprovante de Endereço',
        'Declaração do Imposto de Renda da Empresa',
        'RG e CPF do Sócio - Administrador',
        'Verificação de Processos Judiciais',
        'Busca Geral de Protestos',
        'Consulta de Restrições de Crédito (SPC/SERASA)',
        'Laudo de Vistoria',
        'Contrato Assinado'
    ]
    
    context = {
        'responsaveis': responsaveis,
        'status_choices': Contrato.STATUS_CHOICES,
        'tipo_locatario_choices': Contrato.TIPO_LOCATARIO_CHOICES,
        'tipo_garantia_choices': Contrato.TIPO_GARANTIA_CHOICES,
        'documentos_pf': documentos_pf,
        'documentos_pj': documentos_pj,
    }
    
    return render(request, 'contratos/criar.html', context)


@login_required
def contrato_editar(request, contrato_id):
    """
    View para editar contrato existente
    """
    contrato = get_object_or_404(Contrato, id=contrato_id)
    
    # Verificar permissão: apenas responsável ou admin pode editar
    if contrato.responsavel != request.user and not request.user.is_staff:
        messages.error(request, 'Você não tem permissão para editar este contrato.')
        return redirect('kanban')
    
    if request.method == 'POST':
        try:
            # Salvar status anterior para histórico
            status_anterior = contrato.status
            
            # Atualizar campos
            contrato.nome_negociacao = request.POST.get('nome_negociacao')
            contrato.status = request.POST.get('status')
            contrato.locatario_nome = request.POST.get('locatario_nome')
            contrato.locatario_tipo = request.POST.get('locatario_tipo')
            contrato.locatario_documento = request.POST.get('locatario_documento')
            contrato.locatario_email = request.POST.get('locatario_email', '')
            contrato.locatario_telefone = request.POST.get('locatario_telefone', '')
            contrato.imovel_endereco = request.POST.get('imovel_endereco')
            contrato.imovel_codigo = request.POST.get('imovel_codigo', '')
            contrato.inicio_vigencia = request.POST.get('inicio_vigencia')
            contrato.fim_vigencia = request.POST.get('fim_vigencia')
            contrato.valor_aluguel = request.POST.get('valor_aluguel')
            contrato.tipo_garantia = request.POST.get('tipo_garantia')
            contrato.prazo_fase_dias = request.POST.get('prazo_fase_dias', 5)
            
            # Permitir alterar responsável apenas para admin
            if request.user.is_staff:
                responsavel_id = request.POST.get('responsavel')
                if responsavel_id:
                    contrato.responsavel_id = responsavel_id
            
            # Se status mudou, atualizar data de entrada na fase
            if status_anterior != contrato.status:
                contrato.data_entrada_fase = timezone.now()
                
                # Criar registro no histórico
                HistoricoStatus.objects.create(
                    contrato=contrato,
                    status_anterior=status_anterior,
                    status_novo=contrato.status,
                    alterado_por=request.user,
                    observacao='Status alterado via edição'
                )
            
            contrato.save()
            
            # Processar remoção de anexos
            anexos_remover = request.POST.getlist('remover_anexos')
            if anexos_remover:
                from .models import AnexoContrato
                AnexoContrato.objects.filter(id__in=anexos_remover, contrato=contrato).delete()
            
            # Processar novos anexos
            arquivos = request.FILES.getlist('anexos')
            descricoes = request.POST.getlist('descricoes_anexos')
            
            for i, arquivo in enumerate(arquivos):
                if arquivo:  # Verificar se arquivo foi realmente enviado
                    descricao = descricoes[i] if i < len(descricoes) and descricoes[i] else arquivo.name
                    from .models import AnexoContrato
                    AnexoContrato.objects.create(
                        contrato=contrato,
                        arquivo=arquivo,
                        descricao=descricao,
                        enviado_por=request.user
                    )
                    
                    # Marcar anexos obrigatórios como anexados
                    if 'Laudo de Vistoria' in descricao or 'laudo' in descricao.lower():
                        contrato.laudo_vistoria_anexado = True
                    if 'Contrato Assinado' in descricao or 'assinado' in descricao.lower():
                        contrato.contrato_assinado_anexado = True
                    
                    # Anexos de Análise de Crédito
                    if 'Processos Judiciais' in descricao or 'processos' in descricao.lower():
                        contrato.processos_judiciais_anexado = True
                    if 'Protestos' in descricao or 'protesto' in descricao.lower():
                        contrato.protestos_anexado = True
                    if 'Restrições de Crédito' in descricao or 'SPC' in descricao or 'SERASA' in descricao or 'restrições' in descricao.lower() or 'restricoes' in descricao.lower():
                        contrato.restricoes_credito_anexado = True
            
            # Salvar novamente para atualizar flags de anexos
            contrato.save()
            
            messages.success(request, f'Contrato "{contrato.nome_negociacao}" atualizado com sucesso!')
            return redirect('contratos:detalhe', contrato_id=contrato.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao atualizar contrato: {str(e)}')
    
    # GET - exibir formulário preenchido
    responsaveis = User.objects.filter(is_active=True).order_by('username')
    
    # Documentos necessários por tipo de locatário
    documentos_pf = [
        'Cópia dos Documentos Pessoas: RG/CPF e/ou CNH',
        'Comprovante de Residência',
        'Certidão de Casamento e/ou Atestado de Óbito do Cônjuge',
        'Última Declaração do Imposto de Renda',
        'Verificação de Processos Judiciais',
        'Busca Geral de Protestos',
        'Consulta de Restrições de Crédito (SPC/SERASA)',
        'Laudo de Vistoria',
        'Contrato Assinado'
    ]
    
    documentos_pj = [
        'Contrato Social',
        'Cartão CNPJ',
        'Inscrição Estadual e Municipal',
        'Comprovante de Endereço',
        'Declaração do Imposto de Renda da Empresa',
        'RG e CPF do Sócio - Administrador',
        'Verificação de Processos Judiciais',
        'Busca Geral de Protestos',
        'Consulta de Restrições de Crédito (SPC/SERASA)',
        'Laudo de Vistoria',
        'Contrato Assinado'
    ]
    
    context = {
        'contrato': contrato,
        'responsaveis': responsaveis,
        'status_choices': Contrato.STATUS_CHOICES,
        'tipo_locatario_choices': Contrato.TIPO_LOCATARIO_CHOICES,
        'tipo_garantia_choices': Contrato.TIPO_GARANTIA_CHOICES,
        'documentos_pf': documentos_pf,
        'documentos_pj': documentos_pj,
    }
    
    return render(request, 'contratos/editar.html', context)


@login_required
def baixar_todos_anexos(request, contrato_id):
    """
    View para baixar todos os anexos de um contrato em um arquivo ZIP
    """
    import zipfile
    from django.http import HttpResponse
    import os
    from io import BytesIO
    
    contrato = get_object_or_404(Contrato, id=contrato_id)
    anexos = contrato.anexos.all()
    
    if not anexos:
        messages.error(request, 'Este contrato não possui anexos.')
        return redirect('contratos:detalhe', contrato_id=contrato_id)
    
    # Criar arquivo ZIP em memória
    zip_buffer = BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for anexo in anexos:
            try:
                # Obter nome do arquivo
                nome_arquivo = os.path.basename(anexo.arquivo.name)
                # Adicionar prefixo com descrição
                nome_seguro = f"{anexo.id}_{anexo.descricao[:50]}_{nome_arquivo}"
                
                # Adicionar arquivo ao ZIP
                zip_file.writestr(nome_seguro, anexo.arquivo.read())
            except Exception as e:
                print(f"Erro ao adicionar {anexo.descricao}: {e}")
                continue
    
    # Preparar resposta HTTP
    zip_buffer.seek(0)
    response = HttpResponse(zip_buffer.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename="contrato_{contrato.id}_anexos.zip"'
    
    return response


@login_required
def visualizar_anexo(request, anexo_id):
    """
    View para visualizar anexo inline (sem baixar)
    """
    import os
    import mimetypes
    from django.http import FileResponse, HttpResponse
    from .models import AnexoContrato
    
    anexo = get_object_or_404(AnexoContrato, id=anexo_id)
    
    # Abrir arquivo
    try:
        arquivo = anexo.arquivo.open('rb')
    except Exception as e:
        return HttpResponse(f'Erro ao abrir arquivo: {str(e)}', status=500)
    
    # Determinar content type baseado na extensão
    nome_arquivo = os.path.basename(anexo.arquivo.name)
    content_type, _ = mimetypes.guess_type(nome_arquivo)
    
    # Se não conseguiu determinar, tentar pela extensão
    if not content_type:
        nome_lower = nome_arquivo.lower()
        if nome_lower.endswith('.pdf'):
            content_type = 'application/pdf'
        elif nome_lower.endswith(('.jpg', '.jpeg')):
            content_type = 'image/jpeg'
        elif nome_lower.endswith('.png'):
            content_type = 'image/png'
        elif nome_lower.endswith('.gif'):
            content_type = 'image/gif'
        elif nome_lower.endswith(('.doc', '.docx')):
            content_type = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        else:
            content_type = 'application/octet-stream'
    
    # Criar response
    response = FileResponse(arquivo, content_type=content_type)
    
    # Para PDF e imagens, usar inline
    if content_type in ['application/pdf', 'image/jpeg', 'image/png', 'image/gif']:
        response['Content-Disposition'] = f'inline; filename="{nome_arquivo}"'
    else:
        # Para outros tipos, forçar download
        response['Content-Disposition'] = f'attachment; filename="{nome_arquivo}"'
    
    # Headers adicionais para melhor compatibilidade
    response['X-Content-Type-Options'] = 'nosniff'
    response['Content-Length'] = anexo.arquivo.size
    
    return response
