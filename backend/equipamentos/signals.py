from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Equipamento

@receiver(pre_save, sender=Equipamento)
def log_alteracao_equipamento(sender, instance, **kwargs):
    # Aqui você pode comparar os valores antigos com os novos
    if instance.pk:  # Verifica se o equipamento já existe
        equipamento_antigo = sender.objects.get(pk=instance.pk)
        print(f"Alteração feita por: {instance.modified_by}")  # Você precisa ter esse campo no modelo
        print(f"Nome antes: {equipamento_antigo.nome}, Nome depois: {instance.nome}")
        print(f"Descrição antes: {equipamento_antigo.descricao}, Descrição depois: {instance.descricao}")
