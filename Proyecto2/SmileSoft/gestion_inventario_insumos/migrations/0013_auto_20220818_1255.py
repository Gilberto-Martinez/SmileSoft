# Generated by Django 3.1.13 on 2022-08-18 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0012_auto_20220718_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insumo',
            name='unidad',
            field=models.CharField(choices=[('Paquete', 'Paquete'), ('Caja', 'Caja'), ('Litro', 'Litro')], max_length=12, verbose_name='Unidad'),
        ),
    ]
