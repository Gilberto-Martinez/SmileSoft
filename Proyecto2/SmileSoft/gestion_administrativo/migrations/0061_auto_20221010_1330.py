# Generated by Django 3.1.13 on 2022-10-10 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0060_auto_20221010_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamientoconfirmado',
            name='estado',
            field=models.CharField(choices=[('Realizado', 'Realizado'), ('Confirmado', 'Confirmado'), ('Agendado', 'Agendado')], default='Confirmado', max_length=12),
        ),
    ]
