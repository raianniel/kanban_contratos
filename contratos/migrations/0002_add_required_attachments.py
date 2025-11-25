from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contratos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrato',
            name='laudo_vistoria_anexado',
            field=models.BooleanField(default=False, verbose_name='Laudo de Vistoria Anexado'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='contrato_assinado_anexado',
            field=models.BooleanField(default=False, verbose_name='Contrato Assinado Anexado'),
        ),
    ]
