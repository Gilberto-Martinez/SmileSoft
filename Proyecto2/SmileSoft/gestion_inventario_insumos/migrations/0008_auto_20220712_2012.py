# Generated by Django 3.1.13 on 2022-07-13 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0007_auto_20220712_1439'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='precio',
            field=models.IntegerField(verbose_name='Precio (*):'),
        ),
    ]