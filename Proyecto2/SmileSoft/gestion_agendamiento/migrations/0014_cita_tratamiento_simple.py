# Generated by Django 3.1.13 on 2022-10-19 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0015_tratamientocategoria'),
        ('gestion_agendamiento', '0013_remove_cita_tratamiento_simple'),
    ]

    operations = [
        migrations.AddField(
            model_name='cita',
            name='tratamiento_simple',
            field=models.ForeignKey(limit_choices_to={'tipo_categoria': 'Simple'}, null=True, on_delete=django.db.models.deletion.PROTECT, to='gestion_tratamiento.tratamientocategoria'),
        ),
    ]
