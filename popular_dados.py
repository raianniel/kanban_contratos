#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
"""
import os
import sys
import django
from datetime import date, timedelta
from random import choice, randint

# Configurar Django
sys.path.append("/home/ubuntu/kanban_contratos")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "contratos_project.settings")
django.setup()

from django.contrib.auth.models import User
from contratos.models import Contrato

# Criar usuárioss de exemplo se não existirem
usuarios = []
nomes_usuarios = ["joao.silva", "maria.santos", "carlos.oliveira", "ana.costa"]

for nome in nomes_usuarios:
    user, created = User.objects.get_or_create(
        username=nome,
        defaults={
            "email": f"{nome}@example.com",
            "first_name": nome.split(".")[0].title(),
            "last_name": nome.split(".")[1].title(),
        },
    )
    if created:
        user.set_password("senha123")
        user.save()
        print(f"Usuário criado: {nome}")
    usuarios.append(user)

# Dados de exemplo para contratos
locatarios_pf = [
    "João Pedro Silva",
    "Maria Fernanda Santos",
    "Carlos Eduardo Oliveira",
    "Ana Paula Costa",
    "Ricardo Alves Pereira",
    "Juliana Rodrigues Lima",
    "Fernando Henrique Souza",
    "Patrícia Martins Ferreira",
]

locatarios_pj = [
    "Tech Solutions Ltda",
    "Comércio Brasil S.A.",
    "Serviços Gerais Eireli",
    "Indústria Nacional Ltda",
    "Consultoria Empresarial S.A.",
    "Distribuidora Regional Ltda",
]

enderecos = [
    "Rua das Flores, 123 - Centro",
    "Av. Paulista, 1000 - Bela Vista",
    "Rua Augusta, 456 - Consolação",
    "Av. Brigadeiro Faria Lima, 2000 - Jardim Paulistano",
    "Rua Oscar Freire, 789 - Cerqueira César",
    "Av. Rebouças, 3000 - Pinheiros",
    "Rua Haddock Lobo, 555 - Cerqueira César",
    "Av. Ibirapuera, 2000 - Moema",
    "Rua Pamplona, 145 - Jardins",
    "Av. Angélica, 2500 - Consolação",
]

status_opcoes = [
    "VALIDACAO_DADOS",
    "ANALISE_CREDITO",
    "ELABORACAO_CONTRATO",
    "REQUISICAO_VISTORIA",
    "MINUTA_APROVACAO",
    "ASSINATURA_ELETRONICA",
    "REQUISICAO_LANCAMENTO",
    "CONTRATO_ASSINADO",
]

garantias = ["CAUCAO", "FIADOR", "SEGURO", "TITULO", "NENHUMA"]

# Criar contratos de exemplo
print("\nCriando contratos de exemplo...")
contratos_criados = 0

for i in range(30):
    tipo_locatario = choice(["PF", "PJ"])

    if tipo_locatario == "PF":
        locatario = choice(locatarios_pf)
        documento = f"{randint(100, 999)}.{randint(100, 999)}.{randint(100, 999)}-{randint(10, 99)}"
    else:
        locatario = choice(locatarios_pj)
        documento = f"{randint(10, 99)}.{randint(100, 999)}.{randint(100, 999)}/0001-{randint(10, 99)}"

    endereco = choice(enderecos)
    status = choice(status_opcoes)
    responsavel = choice(usuarios)

    # Datas de vigência
    inicio = date.today() + timedelta(days=randint(-180, 30))
    fim = inicio + timedelta(days=randint(365, 1095))  # 1 a 3 anos

    # Valor do aluguel
    valor = randint(1000, 10000)

    # Prazo da fase (alguns com SLA excedido)
    prazo_fase = choice([3, 5, 7, 10])

    contrato = Contrato.objects.create(
        nome_negociacao=f"Contrato {i+1:03d} - {locatario[:20]}",
        status=status,
        locatario_nome=locatario,
        locatario_tipo=tipo_locatario,
        locatario_documento=documento,
        imovel_endereco=endereco,
        imovel_codigo=f"IMOV-{randint(1000, 9999)}",
        inicio_vigencia=inicio,
        fim_vigencia=fim,
        valor_aluguel=valor,
        tipo_garantia=choice(garantias),
        responsavel=responsavel,
        prazo_fase_dias=prazo_fase,
        possui_anexos=choice([True, False]),
    )

    # Ajustar data_entrada_fase para simular alguns com SLA excedido
    if randint(1, 100) <= 30:  # 30% de chance de estar atrasado
        dias_atras = randint(prazo_fase + 1, prazo_fase + 10)
        from django.utils import timezone

        contrato.data_entrada_fase = timezone.now() - timedelta(days=dias_atras)
        contrato.save()

    contratos_criados += 1
    print(
        f"  Contrato {contratos_criados}: {contrato.nome_negociacao} - {contrato.get_status_display()}"
    )

# Criar alguns contratos cancelados
print("\nCriando contratos cancelados...")
for i in range(3):
    tipo_locatario = choice(["PF", "PJ"])

    if tipo_locatario == "PF":
        locatario = choice(locatarios_pf)
        documento = f"{randint(100, 999)}.{randint(100, 999)}.{randint(100, 999)}-{randint(10, 99)}"
    else:
        locatario = choice(locatarios_pj)
        documento = f"{randint(10, 99)}.{randint(100, 999)}.{randint(100, 999)}/0001-{randint(10, 99)}"

    motivos_cancelamento = [
        "Desistência do locatário",
        "Documentação irregular",
        "Análise de crédito reprovada",
        "Imóvel não disponível",
        "Solicitação do proprietário",
    ]

    contrato = Contrato.objects.create(
        nome_negociacao=f"Contrato Cancelado {i+1} - {locatario[:20]}",
        status="CONTRATO_CANCELADO",
        locatario_nome=locatario,
        locatario_tipo=tipo_locatario,
        locatario_documento=documento,
        imovel_endereco=choice(enderecos),
        imovel_codigo=f"IMOV-{randint(1000, 9999)}",
        tipo_garantia=choice(garantias),
        responsavel=choice(usuarios),
        motivo_cancelamento=choice(motivos_cancelamento),
    )

    contratos_criados += 1
    print(f"  Contrato cancelado {i+1}: {contrato.nome_negociacao}")

print(f"\n✓ Total de {contratos_criados} contratos criados com sucesso!")
print("\nResumo por status:")
from django.db.models import Count

stats = Contrato.objects.values("status").annotate(total=Count("id")).order_by("status")
for stat in stats:
    print(f'  {stat["status"]}: {stat["total"]} contratos')
