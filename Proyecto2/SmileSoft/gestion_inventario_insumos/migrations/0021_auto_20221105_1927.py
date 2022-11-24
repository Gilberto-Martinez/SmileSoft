# Generated by Django 3.1.13 on 2022-11-05 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inventario_insumos', '0020_auto_20221103_2119'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insumo',
            name='calculo_valor',
        ),
        migrations.AddField(
            model_name='insumo',
            name='ud_unitaria',
            field=models.CharField(choices=[('mg', 'ml'), ('ml', 'ml'), ('ampollas', 'amp')], default='ml', max_length=12, verbose_name='Ud. Unitaria'),
        ),
    ]