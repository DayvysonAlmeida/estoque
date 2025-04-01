from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipamentoViewSet,
    EquipamentoAdminViewSet,
    EquipamentoLeitorViewSet,
    HistoricoAlteracoesAPIView,
    HistoricoEquipamentoAPIView,  # Novo import para histórico de um equipamento
    EquipamentosDesligadosAPIView,  # Novo import para lista de equipamentos desligados
    CadastroUsuarioAPIView,
    GerenciarUsuariosAPIView,
    UsuarioAtualAPIView,  # Import existente
)

# Configuração do DefaultRouter para os ViewSets
router = DefaultRouter()
router.register(r'equipamentos', EquipamentoViewSet, basename='equipamentos')
router.register(r'equipamentos-admin', EquipamentoAdminViewSet, basename='equipamento-admin')
router.register(r'equipamentos-leitor', EquipamentoLeitorViewSet, basename='equipamento-leitor')

# URLs do aplicativo
urlpatterns = [
    path('', include(router.urls)),  # Inclui rotas do DefaultRouter
    path('historico/', HistoricoAlteracoesAPIView.as_view(), name='historico-alteracoes'),
    path('historico-equipamento/<int:pk>/', HistoricoEquipamentoAPIView.as_view(), name='historico-equipamento'),  # Novo endpoint para histórico específico de equipamento
    path('equipamentos-desligados/', EquipamentosDesligadosAPIView.as_view(), name='equipamentos-desligados'),  # Novo endpoint para equipamentos desligados
    path('usuarios/cadastrar/', CadastroUsuarioAPIView.as_view(), name='cadastro-usuario'),  # Endpoint de cadastro de usuário
    path('usuarios/', GerenciarUsuariosAPIView.as_view(), name='gerenciar-usuarios'),  # Gerenciar usuários
    path('usuarios/<int:pk>/', GerenciarUsuariosAPIView.as_view(), name='editar-usuario'),  # Editar/Excluir usuários
    path('usuarios/me/', UsuarioAtualAPIView.as_view(), name='usuario-atual'),  # Endpoint para buscar usuário logado
]
