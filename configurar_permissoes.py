#!/usr/bin/env python
"""
Script para configurar grupos de permissões do sistema Kanban
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'contratos_project.settings')
django.setup()

from contratos.permissions import criar_grupos_permissoes

if __name__ == '__main__':
    print("=" * 60)
    print("CONFIGURAÇÃO DE GRUPOS DE PERMISSÕES")
    print("=" * 60)
    print()
    
    criar_grupos_permissoes()
    
    print()
    print("=" * 60)
    print("GRUPOS CRIADOS COM SUCESSO!")
    print("=" * 60)
    print()
    print("Grupos disponíveis:")
    print("  - gerente: Acesso total exceto cancelamento")
    print("  - analista: Validação de dados")
    print("  - analista_credito: Análise de crédito")
    print("  - juridico: Elaboração e aprovação de contratos")
    print("  - vistoriador: Requisição de vistoria")
    print("  - financeiro: Lançamentos financeiros")
    print()
    print("Para adicionar usuários aos grupos, use o Django Admin:")
    print("  http://localhost:8000/admin/auth/user/")
    print()
