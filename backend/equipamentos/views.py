from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, BasePermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count
from django.contrib.auth.models import User, Group
from .models import Equipamento
from .serializers import EquipamentoSerializer
from .pagination import CustomPagination  # Importa a paginação personalizada

# Permissão personalizada para o grupo "Suporte"
class IsSuporte(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.groups.filter(name='Suporte').exists()

# ViewSet padrão de equipamentos
class EquipamentoViewSet(ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    pagination_class = CustomPagination  # Paginação personalizada

# ViewSet para o grupo "Suporte"
class EquipamentoAdminViewSet(ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [IsAuthenticated, IsSuporte]
    pagination_class = CustomPagination  # Paginação para administradores

# ViewSet para leitores (apenas leitura)
class EquipamentoLeitorViewSet(ModelViewSet):
    queryset = Equipamento.objects.all()
    serializer_class = EquipamentoSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination  # Paginação para leitores

# API para retornar estatísticas de histórico de alterações
class HistoricoAlteracoesAPIView(APIView):
    def get(self, request):
        # Contagem de alterações por usuário
        modificacoes_por_usuario = Equipamento.objects.values('modified_by__username').annotate(total=Count('id')).order_by('-total')
        
        # Contagem de alterações por data
        modificacoes_por_data = Equipamento.objects.values('modified_at__date').annotate(total=Count('id')).order_by('-modified_at__date')
        
        return Response({
            'modificacoes_por_usuario': modificacoes_por_usuario,
            'modificacoes_por_data': modificacoes_por_data
        })

# API para listar equipamentos desligados
class EquipamentosDesligadosAPIView(APIView):
    def get(self, request):
        equipamentos_desligados = Equipamento.objects.filter(status='desligado').values(
            'id', 'nome', 'descricao', 'tombamento', 'modified_by__username', 'modified_at'
        )
        return Response(equipamentos_desligados)

# API para cadastro de usuários
class CadastroUsuarioAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        grupo = request.data.get('grupo')

        if not username or not password or not grupo:
            return Response({'error': 'Todos os campos são obrigatórios.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, password=password)
            grupo_obj = Group.objects.get(name=grupo)
            user.groups.add(grupo_obj)
            user.save()
            return Response({'message': 'Usuário criado com sucesso!'}, status=status.HTTP_201_CREATED)
        except Group.DoesNotExist:
            return Response({'error': 'Grupo inválido.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# API para gerenciar usuários
class GerenciarUsuariosAPIView(APIView):
    permission_classes = [IsAuthenticated, IsSuporte]

    def get(self, request):
        usuarios = User.objects.all().values('id', 'username', 'groups__name')
        return Response(usuarios)

    def patch(self, request, pk):
        grupo_nome = request.data.get('grupo')
        try:
            user = User.objects.get(pk=pk)
            grupo = Group.objects.get(name=grupo_nome)
            user.groups.clear()
            user.groups.add(grupo)
            return Response({'message': 'Grupo atualizado com sucesso!'})
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
        except Group.DoesNotExist:
            return Response({'error': 'Grupo não encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.delete()
            return Response({'message': 'Usuário excluído com sucesso!'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'Usuário não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

# API para obter informações do usuário logado
class UsuarioAtualAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        grupo = user.groups.first().name if user.groups.exists() else None
        return Response({
            'username': user.username,
            'grupo': grupo
        })

class HistoricoEquipamentoAPIView(APIView):
    def get(self, request, pk):
        try:
            equipamento = Equipamento.objects.get(pk=pk)
            historico = {
                'nome': equipamento.nome,
                'descricao': equipamento.descricao,
                'status': equipamento.status,
                'tombamento': equipamento.tombamento,
                'modified_by': equipamento.modified_by.username if equipamento.modified_by else None,
                'modified_at': equipamento.modified_at,
            }
            return Response({'historico': historico})
        except Equipamento.DoesNotExist:
            return Response({'error': 'Equipamento não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
