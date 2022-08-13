# Generated by Django 3.1.13 on 2022-08-11 03:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_tratamiento', '0008_tratamientoinsumo_cantidad'),
        ('gestion_historial_clinico', '0004_delete_historialclinico'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TratamientoRealizado',
            new_name='HistorialClinico',
        ),
        migrations.RenameField(
            model_name='historialclinico',
            old_name='id_tratamiento_realizado',
            new_name='id_historial_clinico',
        ),
        migrations.AlterModelTable(
            name='historialclinico',
            table='HistorialClinico',
        ),
    ]
