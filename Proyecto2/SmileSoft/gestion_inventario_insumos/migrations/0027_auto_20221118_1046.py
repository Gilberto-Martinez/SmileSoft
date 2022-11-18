# Generated by Django 3.1.13 on 2022-11-18 13:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0026_auto_20221107_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='ud_unitaria',
            field=models.CharField(choices=[('unidades', 'unidades'), ('g', 'g'), ('mg', 'mg'), ('m', 'm'), ('Caja/s', 'cm'), ('mm', 'mm'), ('l', 'l'), ('ml', 'ml'), ('ampollas', 'amp')], max_length=12, verbose_name='Ud. Unitaria'),
        ),
    ]
