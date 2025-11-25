from django.urls import path
from . import views
from .views_publico import cadastro_publico, cadastro_publico_sucesso

app_name = 'contratos'

urlpatterns = [
    # Rotas públicas (sem necessidade de login)
    path('cadastro/', cadastro_publico, name='cadastro_publico'),
    path('cadastro/sucesso/<int:contrato_id>/', cadastro_publico_sucesso, name='cadastro_publico_sucesso'),
    
    # Rotas protegidas (requerem login)
    path('', views.kanban_view, name='kanban'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('criar/', views.contrato_criar, name='criar'),
    path('<int:contrato_id>/', views.contrato_detalhe, name='detalhe'),
    path('<int:contrato_id>/editar/', views.contrato_editar, name='editar'),
    path('<int:contrato_id>/mudar-status/', views.mudar_status, name='mudar_status'),
    path('<int:contrato_id>/baixar-anexos/', views.baixar_todos_anexos, name='baixar_anexos'),
    path('anexo/<int:anexo_id>/visualizar/', views.visualizar_anexo, name='visualizar_anexo'),
]
