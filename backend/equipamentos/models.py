from django.db import models
from django.contrib.auth.models import User

class Equipamento(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[
            ('disponível', 'Disponível'),
            ('emprestado', 'Emprestado'),
            ('desligado', 'Desligado')  # Novo status para equipamentos descartados ou desligados
        ]
    )
    tombamento = models.CharField(
        max_length=50,
        default='Sem/T',  # Valor padrão quando não for preenchido
        blank=False,  # Torna o campo obrigatório
        null=False  # Garante que o banco de dados não permitirá valores nulos
    )
    modified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Usuário que fez a alteração
    modified_at = models.DateTimeField(auto_now=True)  # Momento da alteração

    def __str__(self):
        return f"{self.nome} - {self.tombamento}"  # Retorna o nome e tombamento para facilitar na exibição
