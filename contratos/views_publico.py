"""
Views públicas (sem necessidade de login) para cadastro de contratos
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import Contrato, HistoricoStatus


@ensure_csrf_cookie
def cadastro_publico(request):
    """
    View pública para cadastro de contratos sem necessidade de login.
    O contrato criado vai direto para o status 'VALIDACAO_DADOS'.
    """
    if request.method == 'POST':
        try:
            # Obter dados do formulário
            contrato = Contrato(
                # Gerar nome da negociação automaticamente
                nome_negociacao=f"Contrato - {request.POST.get('locatario_nome')}",
                status='VALIDACAO_DADOS',  # Status inicial fixo
                locatario_nome=request.POST.get('locatario_nome'),
                locatario_tipo=request.POST.get('locatario_tipo'),
                locatario_documento=request.POST.get('locatario_documento'),
                locatario_email=request.POST.get('locatario_email'),
                locatario_telefone=request.POST.get('locatario_telefone'),
                imovel_endereco=request.POST.get('imovel_endereco'),
                imovel_codigo=request.POST.get('imovel_codigo', ''),
                inicio_vigencia=request.POST.get('inicio_vigencia'),
                fim_vigencia=request.POST.get('fim_vigencia'),
                valor_aluguel=request.POST.get('valor_aluguel'),
                tipo_garantia=request.POST.get('tipo_garantia', 'NENHUMA'),
                observacoes_gerais=request.POST.get('observacoes_gerais', ''),
                responsavel=None,  # Sem responsável inicial
                prazo_fase_dias=5,  # Prazo padrão
            )
            contrato.save()
            
            # Processar anexos (se houver)
            arquivos = request.FILES.getlist('anexos[]')
            tipos_anexo = request.POST.getlist('tipo_anexo[]')
            
            if arquivos:
                from .models import AnexoContrato
                for i, arquivo in enumerate(arquivos):
                    if arquivo:  # Verificar se o arquivo foi realmente enviado
                        tipo = tipos_anexo[i] if i < len(tipos_anexo) else 'Outros'
                        descricao = tipo  # Nome do documento sem sufixo
                        
                        AnexoContrato.objects.create(
                            contrato=contrato,
                            arquivo=arquivo,
                            descricao=descricao,
                            enviado_por=None  # Cadastro público sem usuário
                        )
            
            # Criar registro no histórico
            HistoricoStatus.objects.create(
                contrato=contrato,
                status_anterior='',
                status_novo='VALIDACAO_DADOS',
                alterado_por=None,  # Cadastro público
                observacao='Cadastro realizado pelo cliente via formulário público'
            )
            
            messages.success(
                request, 
                f'Cadastro realizado com sucesso! Seu contrato foi registrado e está em análise. '
                f'Você receberá atualizações no e-mail: {contrato.locatario_email}'
            )
            
            # Redirecionar para página de sucesso
            return redirect('contratos:cadastro_publico_sucesso', contrato_id=contrato.id)
            
        except Exception as e:
            messages.error(request, f'Erro ao realizar cadastro: {str(e)}')
    
    # GET - exibir formulário
    return render(request, 'contratos/cadastro_publico.html')


def cadastro_publico_sucesso(request, contrato_id):
    """
    Página de sucesso após cadastro público
    """
    try:
        contrato = Contrato.objects.get(id=contrato_id)
        return render(request, 'contratos/cadastro_publico_sucesso.html', {
            'contrato': contrato
        })
    except Contrato.DoesNotExist:
        messages.error(request, 'Contrato não encontrado.')
        return redirect('contratos:cadastro_publico')
