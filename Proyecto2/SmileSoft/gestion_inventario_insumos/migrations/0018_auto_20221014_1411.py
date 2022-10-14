# Generated by Django 3.1.13 on 2022-10-14 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0017_auto_20221011_1128'),
    ]

    operations = [
        migrations.AddField(
            model_name='insumo',
            name='cantidad_unitaria',
            field=models.IntegerField(default=0, verbose_name='Cantidad unitaria (*)'),
        ),
        migrations.AddField(
            model_name='insumo',
            name='stock_minimo',
            field=models.IntegerField(default=0, verbose_name='Stock mínimo (*)'),
        ),
        migrations.AddField(
            model_name='insumo',
            name='unidad_x_paquete',
            field=models.IntegerField(default=0, verbose_name='Unidad por pcl (*)'),
        ),
    ]
