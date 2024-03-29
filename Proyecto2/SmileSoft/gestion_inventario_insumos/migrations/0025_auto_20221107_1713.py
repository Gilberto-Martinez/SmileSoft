# Generated by Django 3.1.13 on 2022-11-07 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0024_auto_20221106_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='ud_unitaria',
            field=models.CharField(choices=[('g', 'g'), ('mg', 'mg'), ('m', 'm'), ('Caja/s', 'cm'), ('mm', 'mm'), ('l', 'l'), ('ml', 'ml'), ('ampollas', 'amp')], max_length=12, verbose_name='Ud. Unitaria'),
        ),
        migrations.AlterField(
            model_name='insumo',
            name='unidad',
            field=models.CharField(choices=[('Paquete/s', 'Paquete/s'), ('Caja/s', 'Caja/s')], max_length=12, verbose_name='Unidad de medida'),
        ),
    ]
