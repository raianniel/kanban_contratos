from django.contrib import admin
from .models import Contrato, AnexoContrato, HistoricoStatus


@admin.register(Contrato)
class ContratoAdmin(admin.ModelAdmin):
    list_display = [
        'nome_negociacao',
        'status',
        'locatario_nome',
        'locatario_tipo',
        'responsavel',
        'fim_vigencia',
        'possui_anexos',
        'criado_em'
    ]
    
    def change_view(self, request, object_id, form_url='', extra_context=None):
        """
        Redirecionar edição para formulário de usuário simples
        """
        from django.shortcuts import redirect
        from django.urls import reverse
        return redirect(reverse('contratos:editar', args=[object_id]))
    
    list_filter = [
        'status',
        'locatario_tipo',
        'tipo_garantia',
        'responsavel',
        'criado_em'
    ]
    
    search_fields = [
        'nome_negociacao',
        'locatario_nome',
        'locatario_documento',
        'imovel_endereco',
        'imovel_codigo'
    ]
    
    readonly_fields = [
        'criado_em',
        'atualizado_em',
        'data_entrada_fase'
    ]
    
    fieldsets = (
        ('Informações Principais', {
            'fields': (
                'nome_negociacao',
                'status',
                'responsavel'
            )
        }),
        ('Dados do Locatário', {
            'fields': (
                'locatario_nome',
                'locatario_tipo',
                'locatario_documento'
            )
        }),
        ('Dados do Imóvel', {
            'fields': (
                'imovel_endereco',
                'imovel_codigo'
            )
        }),
        ('Dados do Contrato', {
            'fields': (
                'inicio_vigencia',
                'fim_vigencia',
                'valor_aluguel',
                'tipo_garantia'
            )
        }),
        ('Controle de SLA', {
            'fields': (
                'data_entrada_fase',
                'prazo_fase_dias'
            )
        }),
        ('Cancelamento', {
            'fields': (
                'motivo_cancelamento',
            ),
            'classes': ('collapse',)
        }),
        ('Controle', {
            'fields': (
                'possui_anexos',
                'criado_em',
                'atualizado_em'
            )
        }),
    )
    
    date_hierarchy = 'criado_em'
    ordering = ['-criado_em']


@admin.register(AnexoContrato)
class AnexoContratoAdmin(admin.ModelAdmin):
    list_display = [
        'contrato',
        'descricao',
        'arquivo',
        'enviado_por',
        'enviado_em'
    ]
    
    list_filter = [
        'enviado_em',
        'enviado_por'
    ]
    
    search_fields = [
        'contrato__nome_negociacao',
        'descricao'
    ]
    
    readonly_fields = ['enviado_em']
    
    date_hierarchy = 'enviado_em'
    ordering = ['-enviado_em']


@admin.register(HistoricoStatus)
class HistoricoStatusAdmin(admin.ModelAdmin):
    list_display = [
        'contrato',
        'status_anterior',
        'status_novo',
        'alterado_por',
        'alterado_em'
    ]
    
    list_filter = [
        'status_anterior',
        'status_novo',
        'alterado_em',
        'alterado_por'
    ]
    
    search_fields = [
        'contrato__nome_negociacao',
        'observacao'
    ]
    
    readonly_fields = [
        'contrato',
        'status_anterior',
        'status_novo',
        'alterado_por',
        'alterado_em'
    ]
    
    date_hierarchy = 'alterado_em'
    ordering = ['-alterado_em']
    
    def has_add_permission(self, request):
        # Histórico é criado automaticamente, não deve ser adicionado manualmente
        return False
    
    def has_change_permission(self, request, obj=None):
        # Histórico não deve ser editado
        return False
