# Generated by Django 3.1.13 on 2022-10-11 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0064_auto_20221010_2346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tratamientoconfirmado',
            name='estado',
            field=models.CharField(choices=[('Agendado', 'Agendado'), ('Confirmado', 'Confirmado'), ('Pagado', 'Pagado'), ('Realizado', 'Realizado')], default='Agendado', max_length=12),
        ),
    ]
