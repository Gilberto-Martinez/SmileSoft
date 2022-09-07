# Generated by Django 3.1.13 on 2022-09-05 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0014_auto_20220818_1450'),
        ('gestion_tratamiento', '0010_tratamientoinsumoasignado'),
    ]

    operations = [
        migrations.AddField(
            model_name='tratamiento',
            name='insumos',
            field=models.ManyToManyField(related_name='tratamiento_set', through='gestion_tratamiento.TratamientoInsumoAsignado', to='gestion_inventario_insumos.Insumo'),
        ),
    ]