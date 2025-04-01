from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from equipamentos.models import Equipamento  # Substitua pelo nome do seu app/modelo

# Verificar e criar grupo "Suporte" apenas se não existir
if not Group.objects.filter(name='Suporte').exists():
    suporte = Group.objects.create(name='Suporte')
    content_type = ContentType.objects.get_for_model(Equipamento)
    permissions = Permission.objects.filter(content_type=content_type)
    suporte.permissions.set(permissions)  # Permissões completas

# Verificar e criar grupo "Leitor" apenas se não existir
if not Group.objects.filter(name='Leitor').exists():
    leitor = Group.objects.create(name='Leitor')
    view_permission = Permission.objects.get(codename='view_equipamento')  # Verifica o nome correto
    leitor.permissions.add(view_permission)
