# Generated by Django 3.1.13 on 2022-07-12 17:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0005_auto_20220712_1256'),
    ]

    operations = [
        migrations.RenameField(
            model_name='insumo',
            old_name='descripción_insumo',
            new_name='descripcion_insumo',
        ),
    ]