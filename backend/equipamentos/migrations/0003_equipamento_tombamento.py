# Generated by Django 5.1.7 on 2025-04-01 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('equipamentos', '0002_remove_equipamento_data_cadastro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='equipamento',
            name='tombamento',
            field=models.CharField(default='Sem/T', max_length=50),
        ),
    ]
