# Generated by Django 3.1.13 on 2022-05-03 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0022_auto_20220428_2341'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='es_funcionario',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='es_paciente',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='es_personal_salud',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='es_proveedor',
        ),
        migrations.AlterField(
            model_name='insumo',
            name='precio',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
