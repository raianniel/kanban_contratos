from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


class Contrato(models.Model):
    """
    Modelo para representar contratos de locação no sistema Kanban
    """
    
    # Choices para status do contrato (ordem fixa conforme especificação)
    STATUS_CHOICES = [
        ('VALIDACAO_DADOS', 'Validação de dados'),
        ('ANALISE_CREDITO', 'Análise de crédito'),
        ('ELABORACAO_CONTRATO', 'Elaboração do contrato'),
        ('REQUISICAO_VISTORIA', 'Requisição de vistoria'),
        ('MINUTA_APROVACAO', 'Minuta em aprovação'),
        ('ASSINATURA_ELETRONICA', 'Assinatura eletrônica do contrato'),
        ('REQUISICAO_LANCAMENTO', 'Requisição de lançamento financeiro'),
        ('CONTRATO_ASSINADO', 'Contrato assinado'),
        ('CONTRATO_CANCELADO', 'Contrato cancelado'),
    ]
    
    # Choices para tipo de locatário
    TIPO_LOCATARIO_CHOICES = [
        ('PF', 'Pessoa Física'),
        ('PJ', 'Pessoa Jurídica'),
    ]
    
    # Choices para tipo de garantia
    TIPO_GARANTIA_CHOICES = [
        ('CAUCAO', 'Caução'),
        ('FIADOR', 'Fiador'),
        ('SEGURO', 'Seguro Fiança'),
        ('TITULO', 'Título de Capitalização'),
        ('NENHUMA', 'Nenhuma'),
    ]
    
    # Campos principais
    nome_negociacao = models.CharField(
        max_length=255,
        verbose_name='Nome da Negociação',
        help_text='Identificação da negociação/contrato'
    )
    
    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='VALIDACAO_DADOS',
        verbose_name='Status',
        db_index=True
    )
    
    # Dados do locatário
    locatario_nome = models.CharField(
        max_length=255,
        verbose_name='Nome do Locatário'
    )
    
    locatario_tipo = models.CharField(
        max_length=2,
        choices=TIPO_LOCATARIO_CHOICES,
        default='PF',
        verbose_name='Tipo de Locatário'
    )
    
    locatario_documento = models.CharField(
        max_length=20,
        verbose_name='CPF/CNPJ',
        blank=True
    )
    
    locatario_email = models.EmailField(
        max_length=255,
        verbose_name='E-mail do Locatário',
        blank=True,
        help_text='E-mail para contato'
    )
    
    locatario_telefone = models.CharField(
        max_length=20,
        verbose_name='Telefone do Locatário',
        blank=True,
        help_text='Telefone para contato'
    )
    
    # Dados do imóvel
    imovel_endereco = models.CharField(
        max_length=500,
        verbose_name='Endereço do Imóvel'
    )
    
    imovel_codigo = models.CharField(
        max_length=50,
        verbose_name='Código do Imóvel',
        blank=True
    )
    
    # Dados do contrato
    inicio_vigencia = models.DateField(
        verbose_name='Início da Vigência',
        null=True,
        blank=True
    )
    
    fim_vigencia = models.DateField(
        verbose_name='Fim da Vigência',
        null=True,
        blank=True
    )
    
    valor_aluguel = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Valor do Aluguel',
        null=True,
        blank=True
    )
    
    tipo_garantia = models.CharField(
        max_length=20,
        choices=TIPO_GARANTIA_CHOICES,
        default='NENHUMA',
        verbose_name='Tipo de Garantia'
    )
    
    # Responsável pelo contrato
    responsavel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='contratos',
        verbose_name='Responsável'
    )
    
    # Controle de SLA (Service Level Agreement)
    data_entrada_fase = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Entrada na Fase Atual'
    )
    
    prazo_fase_dias = models.IntegerField(
        default=5,
        verbose_name='Prazo da Fase (dias)',
        help_text='Prazo esperado para conclusão da fase atual'
    )
    
    # Campo para cancelamento
    motivo_cancelamento = models.TextField(
        blank=True,
        verbose_name='Motivo do Cancelamento',
        help_text='Obrigatório ao mover para status CONTRATO_CANCELADO'
    )
    
    # Observações gerais
    observacoes_gerais = models.TextField(
        blank=True,
        verbose_name='Observações Gerais',
        help_text='Campo livre para anotações e informações complementares sobre o contrato'
    )
    
    # Controle de anexos
    possui_anexos = models.BooleanField(
        default=False,
        verbose_name='Possui Anexos'
    )
    
    # Anexos obrigatórios por fase
    laudo_vistoria_anexado = models.BooleanField(
        default=False,
        verbose_name='Laudo de Vistoria Anexado',
        help_text='Obrigatório para mover para fase de Requisição de Vistoria'
    )
    
    contrato_assinado_anexado = models.BooleanField(
        default=False,
        verbose_name='Contrato Assinado Anexado',
        help_text='Obrigatório para mover para fase de Assinatura Eletrônica'
    )
    
    # Anexos de Análise de Crédito
    processos_judiciais_anexado = models.BooleanField(
        default=False,
        verbose_name='Verificação de Processos Judiciais Anexada',
        help_text='Obrigatório para sair da fase de Análise de Crédito'
    )
    
    protestos_anexado = models.BooleanField(
        default=False,
        verbose_name='Busca Geral de Protestos Anexada',
        help_text='Obrigatório para sair da fase de Análise de Crédito'
    )
    
    restricoes_credito_anexado = models.BooleanField(
        default=False,
        verbose_name='Consulta de Restrições de Crédito Anexada',
        help_text='Obrigatório para sair da fase de Análise de Crédito'
    )
    
    # Timestamps
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    
    atualizado_em = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
        ordering = ['status', 'fim_vigencia']
        indexes = [
            models.Index(fields=['status', 'fim_vigencia']),
            models.Index(fields=['responsavel', 'status']),
        ]
    
    def __str__(self):
        return f"{self.nome_negociacao} - {self.get_status_display()}"
    
    def dias_para_vencimento(self):
        """
        Calcula quantos dias faltam para o vencimento do contrato
        Retorna None se fim_vigencia não estiver definido
        """
        if not self.fim_vigencia:
            return None
        
        hoje = timezone.now().date()
        delta = self.fim_vigencia - hoje
        return delta.days
    
    def cor_vencimento(self):
        """
        Retorna a cor do badge de vencimento baseado nos dias restantes
        """
        dias = self.dias_para_vencimento()
        if dias is None:
            return 'secondary'
        if dias < 0:
            return 'danger'  # Vencido
        elif dias <= 30:
            return 'warning'  # Próximo do vencimento
        else:
            return 'success'  # OK
    
    def dias_na_fase_atual(self):
        """
        Calcula quantos dias o contrato está na fase atual
        """
        agora = timezone.now()
        delta = agora - self.data_entrada_fase
        return delta.days
    
    def sla_excedido(self):
        """
        Verifica se o SLA da fase atual foi excedido
        Retorna o número de dias excedidos (positivo) ou None se dentro do prazo
        """
        dias_na_fase = self.dias_na_fase_atual()
        excesso = dias_na_fase - self.prazo_fase_dias
        return excesso if excesso > 0 else None
    
    def cor_coluna_status(self):
        """
        Retorna a cor sugerida para a coluna baseada no status
        """
        cores = {
            'VALIDACAO_DADOS': '#6c757d',  # cinza
            'ANALISE_CREDITO': '#fd7e14',  # laranja
            'ELABORACAO_CONTRATO': '#ffc107',  # mostarda/amarelo
            'REQUISICAO_VISTORIA': '#20c997',  # teal
            'MINUTA_APROVACAO': '#28a745',  # verde
            'ASSINATURA_ELETRONICA': '#ffc107',  # dourado
            'REQUISICAO_LANCAMENTO': '#6f42c1',  # roxo
            'CONTRATO_ASSINADO': '#007bff',  # azul
            'CONTRATO_CANCELADO': '#dc3545',  # vermelho
        }
        return cores.get(self.status, '#6c757d')


class AnexoContrato(models.Model):
    """
    Modelo para anexos relacionados aos contratos
    """
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name='anexos',
        verbose_name='Contrato'
    )
    
    arquivo = models.FileField(
        upload_to='contratos/anexos/%Y/%m/',
        verbose_name='Arquivo'
    )
    
    descricao = models.CharField(
        max_length=255,
        blank=True,
        verbose_name='Descrição'
    )
    
    enviado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Enviado em'
    )
    
    enviado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Enviado por'
    )
    
    class Meta:
        verbose_name = 'Anexo'
        verbose_name_plural = 'Anexos'
        ordering = ['-enviado_em']
    
    def __str__(self):
        return f"Anexo de {self.contrato.nome_negociacao} - {self.descricao}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Atualiza flag de anexos no contrato
        self.contrato.possui_anexos = self.contrato.anexos.exists()
        self.contrato.save(update_fields=['possui_anexos'])


class HistoricoStatus(models.Model):
    """
    Modelo para rastrear mudanças de status dos contratos
    """
    contrato = models.ForeignKey(
        Contrato,
        on_delete=models.CASCADE,
        related_name='historico',
        verbose_name='Contrato'
    )
    
    status_anterior = models.CharField(
        max_length=30,
        choices=Contrato.STATUS_CHOICES,
        verbose_name='Status Anterior'
    )
    
    status_novo = models.CharField(
        max_length=30,
        choices=Contrato.STATUS_CHOICES,
        verbose_name='Status Novo'
    )
    
    alterado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Alterado por'
    )
    
    alterado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Alterado em'
    )
    
    observacao = models.TextField(
        blank=True,
        verbose_name='Observação'
    )
    
    class Meta:
        verbose_name = 'Histórico de Status'
        verbose_name_plural = 'Históricos de Status'
        ordering = ['-alterado_em']
    
    def __str__(self):
        return f"{self.contrato.nome_negociacao}: {self.status_anterior} → {self.status_novo}"
