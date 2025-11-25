from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0002_add_required_attachments'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='processos_judiciais_anexado',
            field=models.BooleanField(default=False, help_text='Obrigatório para sair da fase de Análise de Crédito', verbose_name='Verificação de Processos Judiciais Anexada'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='protestos_anexado',
            field=models.BooleanField(default=False, help_text='Obrigatório para sair da fase de Análise de Crédito', verbose_name='Busca Geral de Protestos Anexada'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='restricoes_credito_anexado',
            field=models.BooleanField(default=False, help_text='Obrigatório para sair da fase de Análise de Crédito', verbose_name='Consulta de Restrições de Crédito Anexada'),
        ),
    ]
