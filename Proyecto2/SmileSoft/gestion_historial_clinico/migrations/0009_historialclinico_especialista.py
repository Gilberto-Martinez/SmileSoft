# Generated by Django 3.1.13 on 2022-10-31 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_administrativo', '0071_auto_20221031_1621'),
        ('gestion_historial_clinico', '0008_auto_20220812_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='historialclinico',
            name='especialista',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_administrativo.especialistasalud'),
        ),
    ]
